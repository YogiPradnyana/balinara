import { createRouter, createWebHistory } from 'vue-router'

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
          path: 'reviews',
          component: Reviews,
          children: [
            { path: '', name: 'AdminReviews', component: ReviewLists },
            { path: 'detail/:id', name: 'AdminReviewDetail', component: ReviewDetail },
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

export default router
