import apiClient from '@/api/axiosInstance' // Impor instance Axios kustom

const AUTH_API_PATH = '/auth/' // Path relatif terhadap baseURL di apiClient

export default {
  /**
   * Registrasi pengguna baru.
   */
  register(userData) {
    return apiClient.post(AUTH_API_PATH + 'register/', userData)
  },

  /**
   * Login pengguna.
   */
  login(credentials) {
    return apiClient.post(AUTH_API_PATH + 'login/', credentials)
  },

  /**
   * Logout pengguna.
   */
  logout() {
    return apiClient.post(AUTH_API_PATH + 'logout/', {}) // Body kosong, token di header
  },

  // =================================================================
  // TAMBAHKAN FUNGSI BARU INI
  // =================================================================
  /**
   * Mengirim authorization code dari Google ke backend.
   * @param {object} authData - Berisi { code: "..." }
   * @returns {Promise<AxiosResponse<any>>}
   */
  googleLogin(authData) {
    // Endpoint ini akan cocok dengan yang kita buat di Django
    return apiClient.post('/auth/social/google/', authData);
  },
  // =================================================================


  /**
   * Mendapatkan detail profil pengguna yang sedang login.
   */
  getProfile() {
    return apiClient.get(AUTH_API_PATH + 'profile/')
  },

  /**
   * Memperbarui profil pengguna.
   */
  updateProfile(profileData) {
    return apiClient.put(AUTH_API_PATH + 'profile/', profileData)
  },

  /**
   * Mengubah password pengguna.
   */
  changePassword(passwordData) {
    return apiClient.put(AUTH_API_PATH + 'change-password/', passwordData)
  },
}
