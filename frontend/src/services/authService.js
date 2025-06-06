// src/services/authService.js
import apiClient from '@/api/axiosInstance' // Impor instance Axios kustom

const AUTH_API_PATH = '/auth/' // Path relatif terhadap baseURL di apiClient

export default {
  /**
   * Registrasi pengguna baru.
   * @param {object} userData - Data pengguna (username, email, password, dll.)
   * @returns {Promise<AxiosResponse<any>>}
   */
  register(userData) {
    return apiClient.post(AUTH_API_PATH + 'register/', userData)
  },

  /**
   * Login pengguna.
   * @param {object} credentials - Kredensial pengguna (email, password)
   * @returns {Promise<AxiosResponse<any>>}
   */
  login(credentials) {
    return apiClient.post(AUTH_API_PATH + 'login/', credentials)
  },

  /**
   * Logout pengguna. Interceptor akan menambahkan token.
   * @returns {Promise<AxiosResponse<any>>}
   */
  logout() {
    return apiClient.post(AUTH_API_PATH + 'logout/', {}) // Body kosong, token di header
  },

  /**
   * Mendapatkan detail profil pengguna yang sedang login. Interceptor akan menambahkan token.
   * @returns {Promise<AxiosResponse<any>>}
   */
  getProfile() {
    return apiClient.get(AUTH_API_PATH + 'profile/')
  },

  /**
   * Memperbarui profil pengguna. Interceptor akan menambahkan token.
   * @param {object|FormData} profileData - Data profil yang akan diupdate.
   * @returns {Promise<AxiosResponse<any>>}
   */
  updateProfile(profileData) {
    // Jika profileData adalah FormData, apiClient (Axios) akan mengatur Content-Type yang benar.
    return apiClient.put(AUTH_API_PATH + 'profile/', profileData)
    // atau apiClient.patch jika backend Anda mendukung partial update untuk profil
  },

  /**
   * Mengubah password pengguna. Interceptor akan menambahkan token.
   * @param {object} passwordData - Data password (old_password, new_password, new_password2)
   * @returns {Promise<AxiosResponse<any>>}
   */
  changePassword(passwordData) {
    return apiClient.put(AUTH_API_PATH + 'change-password/', passwordData)
  },
  // Tambahkan fungsi service lain jika ada
}
