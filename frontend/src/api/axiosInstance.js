// src/api/axiosInstance.js
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  // headers: {
  //   'Content-Type': 'application/json',
  // },
})

// Request Interceptor
apiClient.interceptors.request.use(
  async (config) => {
    // Menggunakan impor dinamis untuk store agar tidak terjadi circular dependency
    // saat file ini mungkin diimpor (secara tidak langsung) oleh authStore.js
    try {
      const { useAuthStore } = await import('@/stores/authStore') // Pastikan path benar
      const authStore = useAuthStore() // Dapatkan instance store di dalam interceptor
      const token = authStore.getToken // Gunakan getter dari store

      if (token && config.headers) {
        // Pastikan config.headers ada
        config.headers.Authorization = `Token ${token}` // Sesuaikan 'Token ' dengan prefix Anda (misal 'Bearer ')
      }
    } catch (e) {
      // Ini bisa terjadi jika Pinia belum siap atau dalam konteks non-Vue.
      // Biarkan request berjalan tanpa token jika store tidak bisa diakses.
      // console.warn("Auth store not available for request interceptor or no token found:", e.message);
    }

    if (config.data instanceof FormData) {
      // Jika data adalah FormData, JANGAN set Content-Type secara manual.
      // Biarkan Axios dan browser menanganinya.
      // Jika sebelumnya ada Content-Type default yang ter-set (misalnya jika tidak dihapus dari axios.create),
      // Anda bisa menghapusnya di sini:
      // delete config.headers['Content-Type']; // Hanya jika ada Content-Type default yang ingin di-override untuk FormData
    } else if (
      config.method !== 'get' &&
      config.method !== 'delete' &&
      !config.headers['Content-Type']
    ) {
      // Jika BUKAN FormData, bukan GET/DELETE (yang biasanya tidak punya body atau Content-Type relevan),
      // dan belum ada Content-Type, maka set ke application/json.
      // Ini mengasumsikan request POST/PUT/PATCH Anda yang bukan FormData adalah JSON.
      config.headers['Content-Type'] = 'application/json'
    }

    return config
  },
  (error) => {
    // Lakukan sesuatu dengan error request
    return Promise.reject(error)
  },
)

// Response Interceptor (Opsional, tapi berguna untuk menangani error global)
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
        // Panggil logout tanpa await agar tidak memblokir jika ada error di logout API
        // dan untuk menghindari loop jika logout juga menghasilkan 401.
        authStore.logout()
        // Anda mungkin ingin mengarahkan pengguna ke halaman login di sini,
        // atau biarkan navigation guard di router yang menanganinya.
        // router.push('/login');
      } catch (e) {
        console.error('Gagal melakukan logout otomatis setelah error 401:', e)
      }
      // Anda juga bisa mencoba refresh token di sini jika menggunakan JWT dengan refresh token
    }
    return Promise.reject(error)
  },
)

export default apiClient
