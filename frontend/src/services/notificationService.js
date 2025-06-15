// Buat helper atau service untuk toast jika sering digunakan
// src/services/notificationService.js (contoh)
import { toast } from 'vue-sonner'

let currentNotificationToastId = null
const CONFIRMATION_TOAST_ID = 'main-confirmation-prompt'

export function showNotification(type, message, options = {}) {
  // Jika ada notifikasi sebelumnya dengan ID yang sama, tutup dulu
  if (currentNotificationToastId) {
    toast.dismiss(currentNotificationToastId)
  }

  // Buat ID baru untuk notifikasi ini
  const newToastId = 'notification-' + Date.now()
  currentNotificationToastId = newToastId

  const toastOptions = {
    id: newToastId,
    duration: options.duration || 4000,
    position: options.position || 'top-right',
    ...options,
    onAutoClose: (t) => {
      // Dipanggil saat toast hilang otomatis
      if (currentNotificationToastId === t.id) {
        currentNotificationToastId = null
      }
      if (options.onAutoClose) options.onAutoClose(t)
    },
    onDismiss: (t) => {
      // Dipanggil saat toast ditutup manual atau otomatis
      if (currentNotificationToastId === t.id) {
        currentNotificationToastId = null
      }
      if (options.onDismiss) options.onDismiss(t)
    },
  }

  switch (type) {
    case 'success':
      toast.success(message, toastOptions)
      break
    case 'error':
      toast.error(message, toastOptions)
      break
    case 'info':
      toast.info(message, toastOptions)
      break
    case 'warning':
      toast.warning(message, toastOptions)
      break
    default:
      toast(message, toastOptions)
  }
}

// Untuk toast konfirmasi kustom Anda, Anda mungkin ingin logika berbeda
// agar tidak ditutup oleh notifikasi standar.
export function showConfirmationToast(component, options = {}) {
  // Jika Anda ingin notifikasi standar hilang saat konfirmasi muncul:
  if (currentNotificationToastId) {
    toast.dismiss(currentNotificationToastId)
    currentNotificationToastId = null
  }

  const toastOptions = {
    id: CONFIRMATION_TOAST_ID,
    duration: Infinity, // Konfirmasi biasanya tidak hilang otomatis
    position: 'top-center',
    ...options, // Izinkan override posisi, dll.
    // className untuk styling spesifik jika perlu
  }

  toast(component, toastOptions)
}

export function dismissCurrentConfirmationToast() {
  toast.dismiss(CONFIRMATION_TOAST_ID)
}
