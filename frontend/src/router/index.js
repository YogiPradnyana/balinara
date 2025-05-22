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
          component: About,
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
          name: 'ChatGemini',   // Nama rute
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
      children: [{ path: 'dashboard', name: 'Dashboard', component: Dashboard }],
    },
  ],
})

export default router