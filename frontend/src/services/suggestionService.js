import apiClient from '@/api/axiosInstance'; // Impor instance axios terpusat Anda

const SUGGESTIONS_API_PATH = '/suggestions/';

const suggestionService = {
  /**
   * Mengambil daftar saran milik user yang sedang login.
   * @returns {Promise}
   */
  getMySuggestions() {
    return apiClient.get(`${SUGGESTIONS_API_PATH}my-suggestions/`);
  },

  /**
   * Membuat suggestion baru.
   * @param {FormData} formData - Data form yang akan dikirim.
   * @returns {Promise}
   */
  create(formData) {
    return apiClient.post(SUGGESTIONS_API_PATH, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },

  // Anda bisa menambahkan fungsi lain di sini nanti, misalnya:
  // getDetail(id) { ... },
  // update(id, data) { ... },
  // delete(id) { ... },
};

export default suggestionService;