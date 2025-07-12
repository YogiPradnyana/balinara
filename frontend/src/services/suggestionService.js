import apiClient from '@/api/axiosInstance';

const SUGGESTIONS_API_PATH = '/suggestions/';

const suggestionService = {
  getAll(params) {
    return apiClient.get(SUGGESTIONS_API_PATH, { params });
  },

  getMySuggestions() {
    return apiClient.get(`${SUGGESTIONS_API_PATH}my-suggestions/`);
  },

  getById(id) {
    return apiClient.get(`${SUGGESTIONS_API_PATH}${id}/`);
  },

  create(formData) {
    // Untuk FormData, Axios akan otomatis mengatur Content-Type menjadi 'multipart/form-data'.
    // Jadi kita tidak perlu menambahkan header di sini.
    return apiClient.post(SUGGESTIONS_API_PATH, formData);
  },

  /**
   * Mengupdate suggestion (misalnya hanya statusnya).
   */
  update(id, data) {
    // Di sini kita secara eksplisit memberitahu bahwa paket data ini adalah JSON.
    return apiClient.patch(`${SUGGESTIONS_API_PATH}${id}/`, data, {
      headers: {
        'Content-Type': 'application/json',
      }
    });
  },

  delete(id) {
    return apiClient.delete(`${SUGGESTIONS_API_PATH}${id}/`);
  },
};

export default suggestionService;
