import apiClient from '@/api/axiosInstance';

const USERS_API_PATH = '/users/';

const userService = {
  /**
   * Mengambil daftar semua pengguna dengan parameter (untuk paginasi, search, dll).
   * @param {object} params 
   * @returns {Promise}
   */
  getAll(params = {}) {
    return apiClient.get(USERS_API_PATH, { params });
  },

  /**
   * Menghapus pengguna berdasarkan ID.
   * @param {number} userId 
   * @returns {Promise}
   */
  deleteById(userId) {
    return apiClient.delete(`${USERS_API_PATH}${userId}/`);
  },

  // Anda bisa menambahkan fungsi lain di sini nanti, seperti:
  // getById(userId) { ... }
  // create(userData) { ... }
  // update(userId, userData) { ... }
};

export default userService;
