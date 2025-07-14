import apiClient from '@/api/axiosInstance';

const SUGGESTIONS_API_PATH = '/suggestions/';

const suggestionService = {
  /**
   * Mengambil daftar semua suggestion untuk halaman admin.
   */
  getAll(params) {
    return apiClient.get(SUGGESTIONS_API_PATH, { params });
  },

  /**
   * Mengambil riwayat saran milik user yang sedang login.
   */
  getMySuggestions() {
    return apiClient.get(`${SUGGESTIONS_API_PATH}my-suggestions/`);
  },

  /**
   * Mengambil detail satu suggestion berdasarkan ID.
   */
  getById(id) {
    return apiClient.get(`${SUGGESTIONS_API_PATH}${id}/`);
  },

  /**
   * Membuat suggestion baru.
   * @param {object} payload - Data form dalam format JSON.
   */
  create(payload) {
    // =================================================================
    // PERBAIKAN UTAMA ADA DI SINI
    // Kita mengirim data sebagai JSON, bukan FormData.
    // =================================================================
    return apiClient.post(SUGGESTIONS_API_PATH, payload, {
      headers: {
        'Content-Type': 'application/json',
      }
    });
  },

  /**
   * Mengupdate suggestion (misalnya hanya statusnya).
   */
  update(id, data) {
    return apiClient.patch(`${SUGGESTIONS_API_PATH}${id}/`, data, {
      headers: {
        'Content-Type': 'application/json',
      }
    });
  },

  /**
   * Menghapus suggestion berdasarkan ID.
   */
  delete(id) {
    return apiClient.delete(`${SUGGESTIONS_API_PATH}${id}/`);
  },

  /**
   * Mengunggah gambar ke endpoint sementara.
   */
  uploadTemporaryImage(file) {
    const formData = new FormData();
    formData.append('image', file);
    return apiClient.post(`${SUGGESTIONS_API_PATH}temp-images/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
};

export default suggestionService;
