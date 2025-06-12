// src/stores/authStore.js
import { defineStore } from 'pinia'
import authService from '@/services/authService' // Sekarang aman untuk diimpor
import router from '@/router' // Impor router untuk navigasi
import { toast } from 'vue-sonner'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    userToken: localStorage.getItem('userToken') || null,
    userData: JSON.parse(localStorage.getItem('userData')) || null,
    status: 'idle', // 'idle', 'loading', 'success', 'error'
    error: null,
    showLoginModal: false, // <-- State baru untuk kontrol modal
    loginRedirectPath: null, // <-- Untuk menyimpan path tujuan setelah login
    // Path untuk redirect JIKA modal DITUTUP tanpa login (khusus dari guard)
    redirectOnClosePath: null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.userToken,
    currentUser: (state) => state.userData,
    getToken: (state) => state.userToken, // Getter ini masih berguna untuk komponen
    isLoading: (state) => state.status === 'loading',
    authError: (state) => state.error,
  },

  actions: {
    _setAuthData(user, token) {
      this.userData = user
      this.userToken = token
      localStorage.setItem('userToken', token)
      localStorage.setItem('userData', JSON.stringify(user))
    },

    _clearAuthData() {
      this.userData = null
      this.userToken = null
      this.status = 'idle'
      this.error = null
      localStorage.removeItem('userToken')
      localStorage.removeItem('userData')
    },

    openLoginModal(redirectPath = null, fromPath = null) {
      this.loginRedirectPath = redirectPath || router.currentRoute.value.fullPath // Simpan path saat ini jika tidak ada redirect spesifik
      // Simpan path asal HANYA jika diberikan (artinya dipicu oleh guard)
      this.redirectOnClosePath = fromPath
      this.showLoginModal = true
    },
    closeLoginModal() {
      const pathToGoBack = this.redirectOnClosePath

      this.showLoginModal = false
      this.redirectOnClosePath = null
      // Kita tidak mereset loginRedirectPath di sini, karena mungkin pengguna
      // menutup lalu membukanya lagi sebelum login. Login action akan membersihkannya

      // Jika ada path untuk kembali, lakukan navigasi
      if (pathToGoBack) {
        // Hindari navigasi yang tidak perlu jika sudah di halaman yang benar
        if (router.currentRoute.value.fullPath !== pathToGoBack) {
          router.push(pathToGoBack)
        }
      }
    },

    async register(credentials) {
      this.status = 'loading'
      this.error = null
      try {
        const response = await authService.register(credentials)
        const { user, token } = response.data
        this._setAuthData(user, token)
        this.status = 'success'
        if (router.currentRoute.value.name !== 'Home') {
          router.push({ name: 'Home' })
        }
        return response
      } catch (error) {
        this.status = 'error'
        this._clearAuthData()
        this.error =
          error.response?.data?.detail ||
          error.response?.data?.message ||
          error.response?.data ||
          'Registration failed.'
        throw this.error
      }
    },

    async login(credentials) {
      this.status = 'loading'
      this.error = null
      try {
        const response = await authService.login(credentials)
        const { user, token } = response.data
        this._setAuthData(user, token)
        this.status = 'success'
        const redirect = this.loginRedirectPath || { name: 'Home' }
        this.loginRedirectPath = null // Clear redirect path
        this.redirectOnClosePath = null // Penting untuk dibersihkan juga
        this.closeLoginModal() // Tutup modal setelah login
        router.push(redirect)
        return response
      } catch (error) {
        this.status = 'error'
        this._clearAuthData()
        let errorMessage = 'Login failed. Please try again.' // Pesan default yang lebih singkat

        if (error.response && error.response.data) {
          const errorData = error.response.data
          // Prioritaskan field 'detail' jika ada (umum untuk error auth DRF)
          if (errorData.detail) {
            errorMessage = errorData.detail
          }
          // Jika tidak ada 'detail', dan errorData adalah string (bisa terjadi untuk beberapa error non-DRF)
          else if (typeof errorData === 'string') {
            errorMessage = errorData
          }
          // Jika errorData adalah objek dan memiliki field 'non_field_errors' (umum untuk validasi form DRF)
          else if (
            errorData.non_field_errors &&
            Array.isArray(errorData.non_field_errors) &&
            errorData.non_field_errors.length > 0
          ) {
            errorMessage = errorData.non_field_errors.join(' ') // Gabungkan semua non_field_errors
          }
          // Jika errorData adalah objek dan punya pesan untuk field spesifik (seperti 'email', 'password')
          // Anda bisa memilih untuk menampilkan pesan error field pertama, atau pesan generik.
          // Untuk kesederhanaan di store, kita bisa tetap pada pesan generik jika 'detail' atau 'non_field_errors' tidak ada.
          // Komponen bisa menampilkan error per field jika diperlukan.
          else if (typeof errorData === 'object' && Object.keys(errorData).length > 0) {
            // Ambil pesan dari field pertama yang memiliki error (jika ada)
            const firstErrorKey = Object.keys(errorData)[0]
            if (Array.isArray(errorData[firstErrorKey]) && errorData[firstErrorKey].length > 0) {
              errorMessage = errorData[firstErrorKey][0] // Ambil pesan pertama dari field error pertama
            }
            // Jika tidak, biarkan errorMessage default
          }
        } else if (error.message) {
          // Jika tidak ada error.response (misalnya, masalah jaringan), gunakan error.message
          errorMessage = error.message
        }

        this.error = errorMessage
        // Melempar error agar komponen bisa menangkapnya dan tahu bahwa login gagal
        // Tidak perlu melempar error.message lagi karena this.error sudah di-set dan bisa diakses komponen
        throw new Error(this.error) // atau throw error; untuk melempar objek error asli
      }
    },

    async logout() {
      this.error = null
      try {
        await authService.logout()
      } catch (error) {
        console.error('Logout API call failed, but user is logged out locally:', error)
      } finally {
        this._clearAuthData()
        this.loginRedirectPath = null
        this.redirectOnClosePath = null
        this.closeLoginModal()
        this.status = 'idle'

        if (router.currentRoute.value.meta.requiresAuth) {
          router.push({ name: 'Home' })
        }
      }
    },

    async fetchProfile() {
      if (!this.isAuthenticated) {
        // Cek menggunakan getter
        // console.log("Not authenticated, skipping fetchProfile.");
        return
      }
      this.status = 'loading'
      this.error = null
      try {
        // Interceptor akan menambahkan token
        const response = await authService.getProfile()
        this.userData = response.data
        localStorage.setItem('userData', JSON.stringify(response.data))
        this.status = 'success'
      } catch (error) {
        this.status = 'error'
        this.error = error.response?.data?.detail || 'Failed to fetch profile.'
        console.error('Fetch profile error:', error)
        // Interceptor response sudah menangani 401 dan memanggil logout jika dikonfigurasi
        // Jika tidak, Anda bisa tambahkan logika logout di sini juga:
        // if (error.response && error.response.status === 401) {
        //   this.logout();
        // }
      }
    },

    async updateProfile(profileData) {
      if (!this.isAuthenticated) throw new Error('User not authenticated')
      this.status = 'loading'
      this.error = null
      try {
        // Interceptor akan menambahkan token
        const response = await authService.updateProfile(profileData)
        this.userData = response.data
        localStorage.setItem('userData', JSON.stringify(response.data))
        this.status = 'success'
        return response
      } catch (error) {
        this.status = 'error'
        this.error =
          error.response?.data?.detail ||
          error.response?.data?.message ||
          'Failed to update profile. Try again.'

        throw new Error(this.error)
      }
    },

    async changePassword(passwordData) {
      if (!this.isAuthenticated) throw new Error('User not authenticated')
      this.status = 'loading'
      this.error = null
      try {
        // Interceptor akan menambahkan token
        const response = await authService.changePassword(passwordData)
        this.status = 'success'
        return response
      } catch (error) {
        this.status = 'error'
        this.error =
          error.response?.data?.detail ||
          error.response?.data?.message ||
          'Failed to change password. Try again.'

        throw new Error(this.error)
      }
    },

    checkAuthStatus() {
      const token = localStorage.getItem('userToken')
      const userDataString = localStorage.getItem('userData')
      if (token && userDataString) {
        this.userToken = token // Set token dulu agar isAuthenticated jadi true
        try {
          this.userData = JSON.parse(userDataString)
          // Dengan interceptor response yang menangani 401, fetchProfile jadi lebih aman
          // untuk memverifikasi token dengan server.
          this.fetchProfile()
        } catch (e) {
          console.error('Failed to parse user data from localStorage', e)
          this._clearAuthData()
        }
      } else {
        this._clearAuthData()
      }
    },
  },
})
