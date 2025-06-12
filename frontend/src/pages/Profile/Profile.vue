<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import Sidebar from '@/components/Sidebar.vue'
import { useAuthStore } from '@/stores/authStore'
import defaultAvatar from '@/assets/images/user_profile/default-avatar.png'
import { toast } from 'vue-sonner'

const authStore = useAuthStore()

const profileForm = ref({
  username: '',
  // Email biasanya tidak diubah, jadi kita tampilkan saja, atau buat read-only
  // email: '',
  phone: '',
})

const initialProfileData = ref({})
const profileImageFile = ref(null) // Untuk file gambar baru
const profileImagePreview = ref(null) // Untuk preview gambar yang dipilih

// State untuk form ganti password
const passwordForm = ref({
  old_password: '',
  new_password: '',
  new_password2: '', // Konfirmasi password baru
})

// State untuk feedback
const profileUpdateStatus = ref('') // 'loading', 'success', 'error'
const profileUpdateError = ref(null)
const passwordChangeStatus = ref('') // 'loading', 'success', 'error'
const passwordChangeError = ref(null)

// Fungsi untuk mengisi form profil saat data user tersedia atau berubah
const populateProfileForm = () => {
  if (authStore.currentUser) {
    const userData = authStore.currentUser
    profileForm.value.username = authStore.currentUser.username || ''
    // profileForm.value.email = authStore.currentUser.email || ''; // Jika ingin di-form juga
    profileForm.value.phone = authStore.currentUser.phone || ''
    profileImagePreview.value = authStore.currentUser.image_url || defaultAvatar
    profileImageFile.value = null

    // Simpan data awal untuk perbandingan
    initialProfileData.value = {
      username: userData.username || '',
      phone: userData.phone || '',
      // Kita tidak melacak image_url di sini karena perubahan gambar ditangani oleh profileImageFile
    }
  } else {
    profileImagePreview.value = defaultAvatar
    profileImageFile.value = null // Reset file yang dipilih setiap kali data di-populate ulang
    initialProfileData.value = { username: '', phone: '' } // Default jika tidak ada user
  }
}

onMounted(() => {
  // Jika data user belum ada saat mounted, fetchProfile mungkin sedang berjalan
  // atau perlu dipanggil jika belum. Kita bisa watch currentUser.
  if (!authStore.currentUser && authStore.isAuthenticated) {
    authStore.fetchProfile().then(populateProfileForm)
  } else {
    populateProfileForm()
  }
})

// Watch currentUser untuk mengupdate form jika data berubah (misal setelah fetchProfile)
watch(
  () => authStore.currentUser,
  (newUser) => {
    if (newUser) {
      populateProfileForm()
    }
  },
  { deep: true },
)

// Computed property untuk mengecek apakah form ganti password sudah valid untuk disubmit
// (yaitu, semua field terisi)
const isChangePasswordFormPopulated = computed(() => {
  return (
    passwordForm.value.old_password.trim() !== '' &&
    passwordForm.value.new_password.trim() !== '' &&
    passwordForm.value.new_password2.trim() !== ''
  )
})

// Computed property untuk mengecek apakah ada perubahan di form profil
const isProfileFormChanged = computed(() => {
  if (!authStore.currentUser) return false // Jika tidak ada user, anggap tidak berubah
  // Cek perubahan pada file gambar
  if (profileImageFile.value !== null) {
    return true
  }
  // Cek perubahan pada field teks
  return (
    profileForm.value.username !== initialProfileData.value.username ||
    profileForm.value.phone !== initialProfileData.value.phone
  )
})

const handleProfileImageChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    profileImageFile.value = file
    // Buat preview URL untuk gambar yang dipilih
    const reader = new FileReader()
    reader.onload = (e) => {
      profileImagePreview.value = e.target.result
    }
    reader.readAsDataURL(file)
  } else {
    // Jika pengguna membatalkan pemilihan file, reset ke gambar sebelumnya atau default
    // dan pastikan profileImageFile.value juga direset agar tidak mengirim data lama/salah.
    profileImageFile.value = null
    profileImagePreview.value = authStore.currentUser?.image_url || defaultAvatar
  }
}

// Fungsi untuk membuka dialog pilih file saat tombol "Change Photo" diklik
const triggerFileInput = () => {
  document.getElementById('profileImageInput').click()
}

const handleProfileUpdate = async () => {
  if (!isProfileFormChanged.value && !profileImageFile.value) {
    // Tambahkan cek profileImageFile juga
    console.log('No changes to submit.')
    // profileUpdateError.value = "No changes to save."; // Opsional: beri feedback
    return
  }

  profileUpdateStatus.value = 'loading'
  profileUpdateError.value = null

  const formData = new FormData()
  formData.append('username', profileForm.value.username)
  // Email biasanya tidak diupdate, jika iya, tambahkan:
  // formData.append('email', profileForm.value.email);
  if (profileForm.value.phone) {
    formData.append('phone', profileForm.value.phone)
  }
  if (profileImageFile.value) {
    formData.append('image', profileImageFile.value, profileImageFile.value.name)
  }

  try {
    await authStore.updateProfile(formData)
    profileUpdateStatus.value = 'success'
    // Setelah berhasil disimpan, update initialProfileData dengan data baru
    // dan reset profileImageFile
    populateProfileForm() // Ini akan mengisi ulang form dan initialProfileData
    // Set timeout untuk menghilangkan pesan sukses
    toast.success('Profile updated successfully!')
  } catch (error) {
    profileUpdateStatus.value = 'error'
    profileUpdateError.value =
      error.message || error.response?.data || 'Failed to update profile. Try again.'
    console.error('Profile update error:', error)
    toast.error(profileUpdateError)
  }
}

const handleChangePassword = async () => {
  passwordChangeStatus.value = 'loading'
  passwordChangeError.value = null

  // Validasi dasar apakah semua field terisi (sebenarnya sudah dihandle oleh :disabled)
  if (!isChangePasswordFormPopulated.value) {
    passwordChangeError.value = 'All password fields are required.'
    passwordChangeStatus.value = 'error'
    toast.error(passwordChangeError)
    return
  }

  if (passwordForm.value.new_password !== passwordForm.value.new_password2) {
    passwordChangeError.value = 'New passwords do not match.'
    passwordChangeStatus.value = 'error'
    toast.error(passwordChangeError)
    return
  }
  // Anda bisa menambahkan validasi panjang minimal password baru di sini juga jika mau
  if (passwordForm.value.new_password.length < 8) {
    // Contoh
    passwordChangeError.value = 'New password must be at least 8 characters long.'
    passwordChangeStatus.value = 'error'
    toast.error(passwordChangeError)
    return
  }

  try {
    await authStore.changePassword({
      old_password: passwordForm.value.old_password,
      new_password: passwordForm.value.new_password,
      new_password2: passwordForm.value.new_password2, // Serializer di backend akan validasi ini
    })
    passwordChangeStatus.value = 'success'
    // Kosongkan field password setelah sukses
    passwordForm.value.old_password = ''
    passwordForm.value.new_password = ''
    passwordForm.value.new_password2 = ''
    toast.success('Password changed successfully!')
  } catch (error) {
    passwordChangeStatus.value = 'error'
    passwordChangeError.value =
      error.message ||
      error.response?.data?.detail ||
      error.response?.data ||
      'Failed to change password. Try again.'
    console.error('Change password error:', error)
    toast.error(passwordChangeError)
  }
}

const getInitials = (username) => {
  if (!username) return 'U'
  return username.charAt(0).toUpperCase()
}
</script>
<template>
  <div
    v-if="authStore.isAuthenticated && authStore.currentUser"
    class="px-6 sm:px-16 lg:px-[140px] pb-24 md:pb-30"
  >
    <main class="mt-10 md:mt-16 flex gap-3 xl:gap-6">
      <Sidebar />
      <div class="p-0 lg:p-4 w-full">
        <h1 class="text-2xl mb-6 md:text-[32px] font-semibold leading-10 md:leading-12">Profile</h1>
        <div class="flex flex-col md:flex-row gap-8 w-full">
          <div class="flex flex-col items-center">
            <div class="relative">
              <img
                v-if="profileImagePreview"
                :src="profileImagePreview"
                alt="User Profile"
                class="size-32 md:size-40 rounded-full object-cover border-2 border-gray-200"
                @error="($event) => ($event.target.src = defaultAvatar)"
              />
              <div
                v-else
                class="size-32 md:size-40 rounded-full border-2 border-gray-200 bg-gray-300 flex items-center justify-center text-gray-600 text-4xl md:text-5xl font-semibold"
              >
                {{ getInitials(authStore.currentUser?.username) }}
              </div>
              <!-- Input file tersembunyi -->
              <input
                type="file"
                id="profileImageInput"
                ref="profileImageInputRef"
                @change="handleProfileImageChange"
                class="hidden"
                accept="image/png, image/jpeg, image/jpg"
              />
            </div>
            <button
              type="button"
              @click="triggerFileInput"
              class="cursor-pointer bg-sur-50 hover:bg-[#e9e9e965] text-sm sm:text-base mt-4 py-2 px-4.5 border border-neu-200 font-medium rounded-full transition-colors"
            >
              Change Photo
            </button>
            <p
              class="w-3/4 md:max-w-60 lg:max-w-52 xl:max-w-80 text-center text-neu-500 text-sm mt-3"
            >
              Photo format must be .jpg, .jpeg, or .png with a maximum file size of 2MB.
            </p>
          </div>
          <div class="flex flex-col flex-1">
            <h3 class="font-semibold mb-4 text-base sm:text-lg">Pengaturan Profil</h3>
            <form @submit.prevent="handleProfileUpdate" class="space-y-4">
              <div class="flex flex-col gap-3">
                <label for="profile-username" class="text-sm font-semibold">Username</label>
                <input
                  id="profile-username"
                  type="text"
                  v-model="profileForm.username"
                  class="w-full border text-sm px-3 py-3 border-neu-200 rounded-full"
                  placeholder="Choose your username"
                />
              </div>
              <div class="flex flex-col gap-3">
                <label for="profile-email" class="text-sm font-semibold"
                  >Email (cannot be changed)</label
                >
                <input
                  id="profile-email"
                  type="email"
                  :value="authStore.currentUser.email"
                  disabled
                  readonly
                  class="w-full border text-sm px-3 py-3 border-neu-200 rounded-full"
                  placeholder="Enter your email"
                />
              </div>
              <div class="flex flex-col gap-3">
                <label for="profile-phone" class="text-sm font-semibold">Phone Number</label>
                <input
                  id="profile-phone"
                  type="tel"
                  v-model="profileForm.phone"
                  class="w-full border text-sm px-3 py-3 border-neu-200 rounded-full"
                  placeholder="Enter your phone number"
                />
              </div>

              <div class="flex justify-end">
                <button
                  type="submit"
                  :disabled="!isProfileFormChanged || profileUpdateStatus === 'loading'"
                  class="disabled:bg-pr-200 disabled:cursor-not-allowed bg-pr-500 transition-colors text-sm sm:text-base font-medium text-neu-50 py-2 px-6 rounded-full"
                >
                  {{ profileUpdateStatus === 'loading' ? 'Saving...' : 'Save Changes' }}
                </button>
              </div>
            </form>
          </div>
        </div>
        <div class="flex mt-8 flex-col md:flex-row gap-5 md:gap-8 w-full">
          <div class="flex flex-col">
            <h3 class="font-semibold text-base sm:text-lg mb-1">Change Password</h3>
            <p class="w-full md:max-w-60 lg:max-w-52 xl:max-w-80 text-neu-500 text-sm">
              Make sure your account uses a long and random password to stay secure.
            </p>
          </div>
          <div class="flex flex-col flex-1">
            <form @submit.prevent="handleChangePassword" class="space-y-4">
              <div class="flex flex-col gap-3">
                <label for="current-password" class="text-sm font-semibold">Current Password</label>
                <input
                  id="current-password"
                  type="password"
                  v-model="passwordForm.old_password"
                  autocomplete="current-password"
                  required
                  class="w-full border text-sm px-3 py-3 border-neu-200 rounded-full"
                />
              </div>
              <div class="flex flex-col gap-3">
                <label for="new-password" class="text-sm font-semibold">New Password</label>
                <input
                  id="new-password"
                  type="password"
                  v-model="passwordForm.new_password"
                  autocomplete="new-password"
                  required
                  class="w-full border text-sm px-3 py-3 border-neu-200 rounded-full"
                />
              </div>
              <div class="flex flex-col gap-3">
                <label for="confirm-password" class="text-sm font-semibold"
                  >Confirmation Password</label
                >
                <input
                  id="confirm-password"
                  type="password"
                  v-model="passwordForm.new_password2"
                  autocomplete="new-password"
                  required
                  class="w-full border text-sm px-3 py-3 border-neu-200 rounded-full"
                />
              </div>

              <div class="flex justify-end">
                <button
                  type="submit"
                  :disabled="!isChangePasswordFormPopulated || passwordChangeStatus === 'loading'"
                  class="disabled:bg-pr-200 bg-pr-500 transition-colors disabled:cursor-not-allowed text-sm sm:text-base font-medium text-neu-50 py-2 px-6 rounded-full"
                >
                  {{ passwordChangeStatus === 'loading' ? 'Changing...' : 'Change Password' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>
