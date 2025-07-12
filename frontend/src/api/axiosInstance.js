// src/api/axiosInstance.js
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
})

// =================================================================
// Request Interceptor (Versi Baru yang Lebih Sederhana dan Kuat)
// =================================================================
apiClient.interceptors.request.use(
  (config) => {
    // Langsung baca token dari localStorage.
    // Ini lebih aman dan menghindari masalah timing dengan Pinia.
    const token = localStorage.getItem('userToken')

    // Jika token ada, tambahkan ke header Authorization.
    if (token && config.headers) {
      config.headers.Authorization = `Token ${token}`
    }
    
    // Kembalikan konfigurasi yang sudah diubah untuk melanjutkan request.
    return config
  },
  (error) => {
    // Jika ada error saat persiapan request, lemparkan.
    return Promise.reject(error)
  },
)

// =================================================================
// Response Interceptor Anda sudah bagus, jadi kita biarkan seperti ini.
// Ini berguna untuk menangani error secara global.
// =================================================================
apiClient.interceptors.response.use(
  (response) => {
    // Setiap status code yang ada di rentang 2xx akan memicu fungsi ini
    return response
  },
  async (error) => {
    // Setiap status code yang ada di luar rentang 2xx akan memicu fungsi ini
    const originalRequest = error.config

    // Contoh: Penanganan error 401 Unauthorized (token tidak valid/kadaluarsa)
    if (error.response && error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true // Tandai request agar tidak di-retry terus menerus

      try {
        // Coba dapatkan authStore untuk memanggil action logout
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
