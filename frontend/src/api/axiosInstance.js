// src/api/axiosInstance.js
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
})

let isLoggingOut = false
// =================================================================
// Request Interceptor ini SEKARANG HANYA BERTUGAS MENAMBAHKAN TOKEN
// =================================================================
apiClient.interceptors.request.use(
  (config) => {
    // Langsung baca token dari localStorage.
    const token = localStorage.getItem('userToken')

    // Jika token ada, tambahkan ke header Authorization.
    if (token && config.headers) {
      config.headers.Authorization = `Token ${token}`
    }

    // Kembalikan konfigurasi untuk melanjutkan request.
    return config
  },
  (error) => {
    return Promise.reject(error)
  },
)

// =================================================================
// Response Interceptor Anda sudah bagus, jadi kita biarkan seperti ini.
// =================================================================
apiClient.interceptors.response.use(
  (response) => {
    return response
  },
  async (error) => {
    const originalRequest = error.config
    if (
      error.response &&
      error.response.status === 401 &&
      !originalRequest._retry &&
      !originalRequest.url.includes('/logout/') &&
      !isLoggingOut
    ) {
      originalRequest._retry = true
      isLoggingOut = true
      try {
        const { useAuthStore } = await import('@/stores/authStore')
        const authStore = useAuthStore()
        console.warn('Token tidak valid atau kadaluarsa. Melakukan logout...')
        authStore.logout()
      } catch (e) {
        console.error('Gagal melakukan logout otomatis setelah error 401:', e)
      }
    }
    return Promise.reject(error)
  },
)

export default apiClient
