import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/authStore'
import About from '@/pages/About.vue'
import Dashboard from '@/pages/admin/Dashboard.vue'
import Destination from '@/pages/Destination.vue'
import DetailDestination from '@/pages/DetailDestination.vue'
import DetailSuggest from '@/pages/DetailSuggest.vue'
import Home from '@/pages/Home.vue'
import Profile from '@/pages/Profile/Profile.vue'
import Review from '@/pages/Profile/Review.vue'
import Suggest from '@/pages/Profile/Suggest.vue'
import Wishlist from '@/pages/Profile/Wishlist.vue'
import Search from '@/pages/Search.vue'
import SuggestSpot from '@/pages/SuggestSpot.vue'
import AdminLayout from '@/layouts/AdminLayout.vue'
import AppLayout from '@/layouts/AppLayout.vue'
// ===============================================
// IMPOR KOMPONEN CHAT GEMINI ANDA
// Asumsi ChatGemini.vue ada di src/components/
// ===============================================
import ChatGemini from '@/components/Chatgemini.vue' // SESUAIKAN PATH INI JIKA BERBEDA!
import WriteReview from '@/pages/WriteReview.vue'
import Users from '@/pages/admin/users/Users.vue'
import UserCreate from '@/pages/admin/users/Create.vue'
import UserEdit from '@/pages/admin/users/Edit.vue'
import UserDetail from '@/pages/admin/users/Detail.vue'
import DestinationCreate from '@/pages/admin/destinations/Create.vue'
import DestinationEdit from '@/pages/admin/destinations/Edit.vue'
import DestinationDetail from '@/pages/admin/destinations/Detail.vue'
import UserLists from '@/pages/admin/users/UserLists.vue'
import Destinations from '@/pages/admin/destinations/Destinations.vue'
import DestinationLists from '@/pages/admin/destinations/DestinationLists.vue'
import CategoryLists from '@/pages/admin/categories/CategoryLists.vue'
import Reviews from '@/pages/admin/testimonials/reviews.vue'
import ReviewLists from '@/pages/admin/testimonials/ReviewLists.vue'
import ReviewDetail from '@/pages/admin/testimonials/Detail.vue'
import Suggestions from '@/pages/admin/suggestions/Suggestions.vue'
import SuggestionLists from '@/pages/admin/suggestions/SuggestionLists.vue'
import SuggestionDetail from '@/pages/admin/suggestions/Detail.vue'
import FacilityLists from '@/pages/admin/facilities/FacilityLists.vue'
// Jika ChatGemini.vue ada di folder 'pages' (misalnya src/pages/ChatGemini.vue), maka:
// import ChatGemini from '@/pages/ChatGemini.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: AppLayout,
      children: [
        // Public
        {
          path: '',
          name: 'Home',
          component: Home,
        },
        {
          path: '/destinations',
          name: 'Destinations',
          component: Destination,
        },
        {
          path: '/destinations/:id',
          name: 'DetailDestinations',
          component: DetailDestination,
          props: true,
        },
        {
          path: '/suggest-spot',
          name: 'SuggestSpot',
          component: SuggestSpot,
        },
        {
          path: '/write-review',
          name: 'WriteReview',
          component: WriteReview,
        },
        {
          path: '/about',
          name: 'About',
          component: About,
        },
        {
          path: '/search',
          name: 'Search',
          component: Search,
        },
        {
          path: '/chat-gemini', // URL yang akan Anda gunakan
          name: 'ChatGemini', // Nama rute
          component: ChatGemini, // Komponen yang akan dirender
        },
        // User Profile
        {
          path: '/user',
          meta: { requiresAuth: true },
          children: [
            { path: 'profile', name: 'Profile', component: Profile },
            { path: 'wishlist', name: 'Wishlist', component: Wishlist },
            { path: 'reviews', name: 'UserReview', component: Review },
            { path: 'suggestions', name: 'UserSuggestion', component: Suggest },
            { path: 'suggestions/:id', name: 'SuggestionDetail', component: DetailSuggest },
          ],
        },
      ],
    },
    {
      path: '/admin',
      component: AdminLayout,
      meta: { requiresAuth: true, requiresAdmin: true },
      children: [
        { path: 'dashboard', name: 'Dashboard', component: Dashboard },
        {
          path: 'users',
          component: Users,
          children: [
            { path: '', name: 'AdminUsers', component: UserLists },
            { path: 'create', name: 'AdminUserCreate', component: UserCreate },
            { path: 'edit/:id', name: 'AdminUserEdit', component: UserEdit },
            { path: 'detail/:id', name: 'AdminUserDetail', component: UserDetail },
          ],
        },
        {
          path: 'destinations',
          component: Destinations,
          children: [
            { path: '', name: 'AdminDestinations', component: DestinationLists },
            { path: 'create', name: 'AdminDestinationCreate', component: DestinationCreate },
            { path: 'edit/:id', name: 'AdminDestinationEdit', component: DestinationEdit },
            { path: 'detail/:id', name: 'AdminDestinationDetail', component: DestinationDetail },
          ],
        },
        {
          path: 'categories',
          name: 'AdminCategories',
          component: CategoryLists,
        },
        {
          path: 'facilities',
          name: 'AdminFacilities',
          component: FacilityLists,
        },
        {
          path: 'reviews',
          component: Reviews,
          children: [
            { path: '', name: 'AdminReviews', component: ReviewLists },
            { path: 'detail/:id', name: 'AdminReviewDetail', component: ReviewDetail },
          ],
        },
        {
          path: 'suggestions',
          component: Suggestions,
          children: [
            { path: '', name: 'AdminSuggestions', component: SuggestionLists },
            { path: 'detail/:id', name: 'AdminSuggestionDetail', component: SuggestionDetail },
          ],
        },
      ],
    },
  ],
  scrollBehavior(to, from, savedPosition) {
    // Jika kembali (back/forward), pakai posisi sebelumnya
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 } // Scroll ke atas setiap halaman berubah
    }
  },
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore() // Dapatkan instance store di dalam guard

  const needsAuth = to.meta.requiresAuth
  const needsAdmin = to.meta.requiresAdmin

  // 1. Cek apakah pengguna sudah terautentikasi (mungkin token ada tapi belum fetch profile)
  // Jika checkAuthStatus belum dipanggil atau sedang berjalan, state isAuthenticated mungkin belum akurat
  // Anda bisa memanggil checkAuthStatus di App.vue onMounted untuk memastikan state awal benar.
  // Untuk guard ini, kita andalkan state isAuthenticated yang ada saat ini.

  if (needsAuth && !authStore.isAuthenticated) {
    // Jika rute memerlukan autentikasi dan pengguna belum login:
    console.log(`Route ${to.name} requires auth. User not authenticated. Opening login modal.`)
    // Panggil action untuk membuka modal login.
    // Simpan path tujuan agar setelah login bisa redirect ke sana.
    authStore.openLoginModal(to.fullPath, from.fullPath)

    // Jika halaman saat ini (from) adalah halaman publik, biarkan pengguna tetap di sana
    // sambil modal login muncul.
    // Jika pengguna mencoba langsung akses URL terproteksi, mereka akan melihat halaman
    // yang kosong/loading sebentar lalu modal muncul.
    // Kita bisa memutuskan untuk mengizinkan navigasi ke halaman tujuan (dan halaman itu
    // yang akan menampilkan "Anda harus login" atau konten terbatas + modal),
    // ATAU kita bisa mencegah navigasi dan tetap di halaman 'from' (jika ada).

    // Opsi A: Izinkan navigasi, biarkan komponen tujuan menampilkan modal (lebih umum untuk SPA)
    // Komponen di 'to.name' harus memeriksa authStore.showLoginModal
    next()

    // Opsi B: Mencegah navigasi ke rute terproteksi dan tetap di halaman 'from' jika valid,
    // atau redirect ke Home jika 'from' tidak ada (misalnya, direct URL access).
    // Ini bisa sedikit membingungkan UX jika modal muncul di atas halaman yang salah.
    /*
    if (from.name) { // Jika ada halaman sebelumnya
      next(false); // Batalkan navigasi saat ini, modal akan muncul di atas halaman 'from'
    } else { // Jika akses langsung via URL
      next({ name: 'Home' }); // Redirect ke Home, modal akan muncul di atas Home
    }
    */
  } else if (
    needsAdmin &&
    (!authStore.isAuthenticated ||
      (authStore.currentUser?.role !== 'admin' && authStore.currentUser?.is_staff !== true))
  ) {
    // Jika rute memerlukan admin, tetapi pengguna bukan admin (atau belum login sama sekali):
    console.log(`Route ${to.name} requires admin. Access denied.`)
    // Redirect ke halaman yang aman, misalnya halaman utama atau halaman "Unauthorized"
    if (authStore.isAuthenticated) {
      // Pengguna login tapi bukan admin
      next({ name: 'UnauthorizedAccess', replace: true }) // Buat rute 'UnauthorizedAccess'
    } else {
      // Pengguna belum login dan mencoba akses halaman admin
      authStore.openLoginModal(to.fullPath, from.fullPath)
      next({ name: 'Home', replace: true }) // Arahkan ke Home, modal akan muncul
    }
  } else {
    // Jika tidak ada restriksi, atau pengguna memenuhi syarat, lanjutkan navigasi
    // Jika modal login terbuka karena navigasi sebelumnya, tutup sekarang
    if (authStore.showLoginModal && to.name !== from.name && !needsAuth && !needsAdmin) {
      // Tutup jika navigasi ke rute publik
      // Ini mungkin perlu logika lebih hati-hati agar tidak menutup modal yang sengaja dibuka pengguna
      // authStore.closeLoginModal();
    }
    next()
  }
})

export default router
