<script setup>
import Subtract from '@/components/icons/Subtract.vue'
import ArrowDown from '@/components/icons/ArrowDown.vue'
import { ref, watchEffect, watch } from 'vue'
import { useCategoryStore } from '@/stores/categoryStore'
import { useFacilityStore } from '@/stores/facilityStore'

const props = defineProps({
  initialData: {
    type: Object,
    default: () => ({}),
  },
  isEditMode: {
    type: Boolean,
    default: false,
  },
  isLoading: {
    type: Boolean,
    default: false,
  },
  errors: { type: Object, default: null },
  isReadOnly: {
    type: Boolean,
    default: false,
  },
})
const emit = defineEmits(['submit'])

const formData = ref({
  name: '',
  description: '',
  ticket_price_range: '',
  is_published: false,
  category_ids: [],
  facility_ids: [],
  address_data: {
    street: '',
    sub_district: '',
    district: '',
    regency: '',
    latitude: null,
    longitude: null,
  },
  contact_data: {
    phone: '',
    mail: '',
  },
})

const minPrice = ref('')
const maxPrice = ref('')

const categoryStore = useCategoryStore()
const facilityStore = useFacilityStore()

if (categoryStore.allCategories.length === 0) categoryStore.fetchCategories()
if (facilityStore.allFacilities.length === 0) facilityStore.fetchFacilities()

// 4. "Pengawas" yang akan mengisi form jika ini adalah mode Edit
watchEffect(() => {
  if (props.isEditMode && props.initialData && props.initialData.id) {
    formData.value.name = props.initialData.name || ''
    formData.value.description = props.initialData.description || ''
    formData.value.ticket_price_range = props.initialData.ticket_price_range || ''
    formData.value.is_published = props.initialData.is_published || false
    formData.value.category_ids = props.initialData.categories?.map((c) => c.id) || []
    formData.value.facility_ids = props.initialData.facilities?.map((f) => f.id) || []
    formData.value.address_data = { ...props.initialData.address }
    formData.value.contact_data = { ...props.initialData.contact }
  }
})

watch([minPrice, maxPrice], ([newMin, newMax]) => {
  // Membersihkan nilai dari titik atau koma jika ada (untuk perhitungan)
  const cleanMin = newMin.replace(/\D/g, '')
  const cleanMax = newMax.replace(/\D/g, '')

  if (cleanMin && cleanMax) {
    // Jika keduanya diisi, format menjadi "Rp X - Rp Y"
    formData.value.ticket_price_range = `Rp ${cleanMin} - Rp ${cleanMax}`
  } else if (cleanMin) {
    // Jika hanya min yang diisi
    formData.value.ticket_price_range = `Mulai dari Rp ${cleanMin}`
  } else if (cleanMax) {
    // Jika hanya max yang diisi
    formData.value.ticket_price_range = `Hingga Rp ${cleanMax}`
  } else {
    // Jika keduanya kosong
    formData.value.ticket_price_range = ''
  }
})

watchEffect(() => {
  if (props.isEditMode && props.initialData && props.initialData.id) {
    formData.value.ticket_price_range = props.initialData.ticket_price_range || ''

    const priceString = props.initialData.ticket_price_range || ''
    if (priceString.includes(' - ')) {
      const parts = priceString.split(' - ')
      minPrice.value = parts[0] || ''
      maxPrice.value = parts[1] || ''
    } else {
      minPrice.value = priceString
      maxPrice.value = ''
    }
  }
})

function handleSubmit() {
  emit('submit', formData.value)
}
</script>
<template>
  <form @submit.prevent="handleSubmit" class="space-y-6">
    <div class="flex flex-col lg:flex-row gap-6 lg:gap-8">
      <!-- Form Left -->
      <div
        class="p-4 w-full lg:w-1/2 xl:w-2/3 border border-neu-100 flex flex-col gap-6 rounded-3xl"
      >
        <div class="flex flex-col gap-3">
          <label for="name" class="text-base font-semibold">Name</label>
          <input
            v-model="formData.name"
            type="text"
            id="name"
            :disabled="isReadOnly"
            placeholder="e.g., Hidden Gem Beach Club"
            class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full"
            :class="{ 'border-red-500': errors?.name, 'bg-[#F2F2F2]': isReadOnly }"
          />
          <p v-if="errors?.name" class="mt-1 text-xs text-red-500">
            {{ errors.name[0] }}
          </p>
        </div>
        <div class="flex flex-col gap-3">
          <label for="category" class="text-base font-semibold">Category</label>
          <div class="flex flex-wrap gap-x-6 gap-y-3">
            <label
              v-for="cat in categoryStore.allCategories"
              :key="cat.id"
              class="flex items-center cursor-pointer"
            >
              <input
                type="checkbox"
                :value="cat.id"
                v-model="formData.category_ids"
                :disabled="isReadOnly"
                class="h-4 w-4 rounded border-gray-300"
              />
              <span class="ml-2 text-sm text-gray-700">{{ cat.name }}</span>
            </label>
          </div>
        </div>
        <div class="flex flex-col gap-3">
          <label for="descriptions" class="text-base font-semibold">Descriptions</label>
          <textarea
            v-model="formData.description"
            id="descriptions"
            rows="7"
            :disabled="isReadOnly"
            placeholder="Tell us what makes this place special..."
            class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-3xl"
            :class="{ 'border-red-500': errors?.description, 'bg-[#F2F2F2]': isReadOnly }"
          ></textarea>
          <p v-if="errors?.description" class="mt-1 text-xs text-red-500">
            {{ errors?.description[0] }}
          </p>
        </div>
        <div class="flex flex-col gap-3">
          <label class="text-base font-semibold">Facilities</label>
          <div class="flex flex-wrap gap-x-6 gap-y-3">
            <label
              v-for="fac in facilityStore.allFacilities"
              :key="fac.id"
              class="flex items-center cursor-pointer"
            >
              <input
                type="checkbox"
                :value="fac.id"
                v-model="formData.facility_ids"
                class="h-4 w-4 rounded border-gray-300"
                :disabled="isReadOnly"
              />
              <span class="ml-2 text-sm text-neu-900">{{ fac.name }}</span>
            </label>
          </div>
        </div>

        <div class="flex flex-col gap-3">
          <label class="text-base md:text-lg font-semibold">Entrance Ticket</label>
          <div class="flex gap-2.5 items-center w-full">
            <input
              type="text"
              v-model="minPrice"
              :disabled="isReadOnly"
              placeholder="e.g., Rp 50.000 or 'Free'"
              class="px-3 py-3 text-sm w-full border placeholder:text-neu-500 border-neu-200 rounded-full"
              :class="{ 'bg-[#F2F2F2]': isReadOnly }"
            />
            <Subtract class="min-w-2" />
            <input
              type="text"
              v-model="maxPrice"
              :disabled="isReadOnly"
              placeholder="e.g., Rp 100.000"
              class="px-3 py-3 text-sm w-full border placeholder:text-neu-500 border-neu-200 rounded-full"
              :class="{ 'bg-[#F2F2F2]': isReadOnly }"
            />
          </div>
        </div>

        <div class="flex flex-col gap-3">
          <div class="space-x-2">
            <h3 class="text-base font-semibold">Contact</h3>
            <p class="text-sm font-medium text-neu-500">Opsional</p>
          </div>
          <label class="text-sm font-semibold">Phone Number</label>
          <input
            v-model="formData.contact_data.phone"
            type="text"
            :disabled="isReadOnly"
            placeholder="e.g., +62 812 3456 7890"
            class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full"
            :class="{ 'border-red-500': errors?.contact?.phone, 'bg-[#F2F2F2]': isReadOnly }"
          />
          <p v-if="errors?.contact?.phone" class="mt-1 text-xs text-red-500">
            {{ errors?.contact?.phone[0] }}
          </p>
          <label class="text-sm font-semibold mt-1">Mail</label>
          <input
            v-model="formData.contact_data.mail"
            type="text"
            :disabled="isReadOnly"
            placeholder="e.g., info@spot.com"
            class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full"
            :class="{ 'border-red-500': errors?.contact?.mail, 'bg-[#F2F2F2]': isReadOnly }"
          />
          <p v-if="errors?.contact?.mail" class="mt-1 text-xs text-red-500">
            {{ errors?.contact?.mail[0] }}
          </p>
        </div>

        <div class="flex flex-col gap-3">
          <div class="text-base font-semibold">Photo</div>
          <p class="text-sm text-neu-500">
            Manajemen foto (upload/delete) bisa dilakukan setelah destinasi ini dibuat/disimpan.
          </p>
        </div>
      </div>

      <!-- Form Right -->
      <div
        class="p-4 w-full flex flex-col gap-6 lg:w-1/2 xl:w-1/3 border h-fit border-neu-100 rounded-3xl"
      >
        <!-- Map -->
        <div class="flex flex-col gap-3">
          <label class="text-base font-semibold">Map Location</label>
          <div class="w-full h-62 rounded-3xl overflow-hidden">
            <iframe
              class="w-full h-full"
              src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d126916.55586267437!2d115.0919508!3d-8.4095178!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x2dd219b8c6d957b3%3A0x5030bfbca83c260!2sBali!5e0!3m2!1sen!2sid!4v1685538498765!5m2!1sen!2sid"
              loading="lazy"
              referrerpolicy="no-referrer-when-downgrade"
            ></iframe>
          </div>
        </div>

        <!-- Street -->
        <div class="flex flex-col gap-3">
          <label for="street" class="text-base font-semibold">Street</label>
          <input
            id="street"
            v-model="formData.address_data.street"
            type="text"
            :disabled="isReadOnly"
            placeholder="e.g., Jalan Pantai Kuta"
            class="px-3 py-3 text-sm border border-gray-300 rounded-full"
            :class="{ 'border-red-500': errors?.address_data?.street, 'bg-[#F2F2F2]': isReadOnly }"
          />
          <p v-if="errors?.address_data?.street" class="mt-1 text-xs text-red-500">
            {{ errors?.address_data?.street[0] }}
          </p>
        </div>

        <!-- Sub-district -->
        <div class="flex flex-col gap-3">
          <label for="sub_district" class="text-base font-semibold">Sub-district</label>
          <input
            id="sub_district"
            v-model="formData.address_data.sub_district"
            type="text"
            :disabled="isReadOnly"
            placeholder="e.g., Legian"
            class="px-3 py-3 text-sm border border-gray-300 rounded-full"
            :class="{
              'border-red-500': errors?.address_data?.sub_district,
              'bg-[#F2F2F2]': isReadOnly,
            }"
          />
          <p v-if="errors?.address_data?.sub_district" class="mt-1 text-xs text-red-500">
            {{ errors?.address_data?.sub_district[0] }}
          </p>
        </div>
        <!-- District -->
        <div class="flex flex-col gap-3">
          <label for="district" class="text-base font-semibold">District</label>
          <input
            id="district"
            v-model="formData.address_data.district"
            type="text"
            :disabled="isReadOnly"
            placeholder="e.g., Kuta"
            class="px-3 py-3 text-sm border border-gray-300 rounded-full"
            :class="{
              'border-red-500': errors?.address_data?.district,
              'bg-[#F2F2F2]': isReadOnly,
            }"
          />
          <p v-if="errors?.address_data?.district" class="mt-1 text-xs text-red-500">
            {{ errors?.address_data?.district[0] }}
          </p>
        </div>

        <!-- Regency -->
        <div class="flex flex-col gap-3">
          <label for="regency" class="text-base font-semibold">Regency</label>
          <input
            v-model="formData.address_data.regency"
            id="regency"
            type="text"
            :disabled="isReadOnly"
            placeholder="e.g., Badung"
            class="px-3 py-3 text-sm border border-gray-300 rounded-full"
            :class="{ 'border-red-500': errors?.address_data?.regency, 'bg-[#F2F2F2]': isReadOnly }"
          />
          <p v-if="errors?.address_data?.regency" class="mt-1 text-xs text-red-500">
            {{ errors?.address_data?.regency[0] }}
          </p>
        </div>

        <!-- Latitude & Longitude -->
        <div class="flex flex-col gap-3">
          <div class="space-x-2">
            <h3 class="text-base font-semibold">Coordinate</h3>
            <p class="text-sm font-medium text-neu-500">Opsional</p>
          </div>
          <div class="flex flex-col sm:flex-row gap-6 sm:gap-4">
            <div class="flex flex-col gap-3 w-full">
              <label for="latitude" class="font-semibold text-sm mt-1">Latitude</label>
              <input
                v-model="formData.address_data.latitude"
                id="latitude"
                type="text"
                :disabled="isReadOnly"
                placeholder="e.g., -8.709201"
                class="px-3 py-3 text-sm border w-full placeholder:text-neu-500 border-neu-200 rounded-full"
                :class="{ 'bg-[#F2F2F2]': isReadOnly }"
              />
            </div>
            <div class="flex flex-col gap-3 w-full">
              <label for="longitude" class="font-semibold text-sm mt-1">Longitude</label>
              <input
                v-model="formData.address_data.longitude"
                id="longitude"
                type="text"
                :disabled="isReadOnly"
                placeholder="e.g., 115.168263"
                class="px-3 py-3 text-sm border w-full placeholder:text-neu-500 border-neu-200 rounded-full"
                :class="{ 'bg-[#F2F2F2]': isReadOnly }"
              />
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="flex gap-2.5 items-center">
      <button
        type="submit"
        :disabled="isLoading"
        :class="{ hidden: isReadOnly }"
        class="px-6 py-2 flex gap-2 items-center cursor-pointer hover:bg-pr-600 justify-center text-sm md:text-base font-medium leading-6 bg-pr-500 rounded-full text-neu-50"
      >
        {{ isLoading ? 'Saving...' : isEditMode ? 'Save' : 'Create' }}
      </button>
      <RouterLink
        :to="{ name: 'AdminDestinations' }"
        type="button"
        class="px-6 py-2 flex gap-2 items-center cursor-pointer hover:bg-[#F0F0F0] justify-center text-sm md:text-base font-medium leading-6 bg-sur-50 rounded-full border border-neu-900"
      >
        {{ isReadOnly ? 'Back' : 'Cancel' }}
      </RouterLink>
    </div>
  </form>
</template>
