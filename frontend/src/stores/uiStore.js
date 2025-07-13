// frontend/src/stores/uiStore.js

import { defineStore } from 'pinia'

export const useUiStore = defineStore('ui', {
  state: () => ({
    isLightboxVisible: false,
    lightboxImages: [],
    lightboxIndex: 0,
  }),
  actions: {
    openLightbox(images, startIndex = 0) {
      this.lightboxImages = images
      this.lightboxIndex = startIndex
      this.isLightboxVisible = true
    },
    closeLightbox() {
      this.isLightboxVisible = false
    },
  },
})
