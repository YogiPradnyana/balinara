// src/stores/authStore.js
import { defineStore } from 'pinia'
import authService from '@/services/authService' // Sekarang aman untuk diimpor
import router from '@/router' // Impor router untuk navigasi
import { toast } from 'vue-sonner'
import { useChatStore } from './chatStore'

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
      if (pathToGoBack) {
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
        this.error = error.response?.data?.detail || 'Registration failed.'
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
        this.loginRedirectPath = null
        this.redirectOnClosePath = null
        this.closeLoginModal()
        router.push(redirect)
        return response
      } catch (error) {
        this.status = 'error'
        this._clearAuthData()
        let errorMessage = 'Login failed. Please try again.'
        if (error.response && error.response.data) {
            const errorData = error.response.data
            if (errorData.detail) errorMessage = errorData.detail
            else if (typeof errorData === 'string') errorMessage = errorData
            else if (errorData.non_field_errors) errorMessage = errorData.non_field_errors.join(' ')
        } else if (error.message) {
            errorMessage = error.message
        }
        this.error = errorMessage
        throw new Error(this.error)
      }
    },
    
    // =================================================================
    // ACTION BARU UNTUK GOOGLE LOGIN DITAMBAHKAN DI SINI
    // =================================================================
    async handleGoogleLogin(authData) {
      this.status = 'loading';
      this.error = null;
      try {
        // Panggil service yang akan mengirim 'code' ke backend
        const response = await authService.googleLogin(authData);
        
        // Backend akan mengembalikan data user dan token seperti login biasa
        const { user, token } = response.data;
        
        // Gunakan helper yang sudah ada untuk menyimpan data
        this._setAuthData(user, token);
        this.status = 'success';
        
        // Tutup modal dan redirect ke halaman tujuan
        const redirect = this.loginRedirectPath || { name: 'Home' };
        this.loginRedirectPath = null;
        this.redirectOnClosePath = null;
        this.closeLoginModal(); // Tutup modal jika terbuka
        router.push(redirect);

      } catch (error) {
        this.status = 'error';
        this._clearAuthData();
        this.error = error.response?.data?.detail || 'Google login failed.';
        toast.error(this.error) // Tampilkan notifikasi error
        throw this.error;
      }
    },
    // =================================================================

    async logout() {
      this.error = null
      try {
        const chatStore = useChatStore()
        await authService.logout()
        chatStore.clearSession()
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
      if (!this.isAuthenticated) return
      this.status = 'loading'
      this.error = null
      try {
        const response = await authService.getProfile()
        this.userData = response.data
        localStorage.setItem('userData', JSON.stringify(response.data))
        this.status = 'success'
      } catch (error) {
        this.status = 'error'
        this.error = error.response?.data?.detail || 'Failed to fetch profile.'
        console.error('Fetch profile error:', error)
      }
    },

    async updateProfile(profileData) {
      // ...
    },

    async changePassword(passwordData) {
      // ...
    },

    checkAuthStatus() {
      const token = localStorage.getItem('userToken')
      const userDataString = localStorage.getItem('userData')
      if (token && userDataString) {
        this.userToken = token
        try {
          this.userData = JSON.parse(userDataString)
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
