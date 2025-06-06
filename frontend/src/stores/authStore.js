// src/stores/authStore.js
import { defineStore } from 'pinia'
import authService from '@/services/authService' // Sekarang aman untuk diimpor
import router from '@/router' // Impor router untuk navigasi

export const useAuthStore = defineStore('auth', {
  state: () => ({
    userToken: localStorage.getItem('userToken') || null,
    userData: JSON.parse(localStorage.getItem('userData')) || null,
    status: 'idle', // 'idle', 'loading', 'success', 'error'
    error: null,
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
      localStorage.removeItem('userToken')
      localStorage.removeItem('userData')
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
        const redirectPath = router.currentRoute.value.query.redirect || { name: 'Home' }
        router.push(redirectPath)
        return response
      } catch (error) {
        this.status = 'error'
        this._clearAuthData()
        this.error =
          error.response?.data?.detail ||
          error.response?.data?.message ||
          error.response?.data ||
          'Login failed.'
        throw this.error
      }
    },

    async logout() {
      this.status = 'loading'
      this.error = null
      try {
        await authService.logout()
      } catch (error) {
        console.error('Logout API call failed, but user is logged out locally:', error)
      } finally {
        this._clearAuthData()
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
        this.error = error.response?.data || 'Failed to update profile.'
        throw this.error
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
        this.error = error.response?.data || 'Failed to change password.'
        throw this.error
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
