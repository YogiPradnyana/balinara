import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import AboutView from '@/views/AboutView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // Public
    {
      path: '/',
      name: 'Home',
      component: HomeView,
    },
    {
      path: '/destinations',
      name: 'Destinations',
      component: AboutView,
    },
    {
      path: '/destinations/:id',
      name: 'DetailDestinations',
      component: AboutView,
      props: true,
    },
    {
      path: '/suggest',
      name: 'Suggest',
      component: AboutView,
    },
    {
      path: '/review',
      name: 'Review',
      component: AboutView,
    },
    {
      path: '/about',
      name: 'About',
      component: AboutView,
    },

    // User Profile
    {
      path: '/profile',
      component: AboutView,
      children: [
        { path: '', name: 'Profile', component: AboutView },
        { path: 'wishlist', name: 'Wishlist', component: AboutView },
        { path: 'reviews', name: 'UserReviews', component: AboutView },
        { path: 'suggestions', name: 'UserSuggestions', component: AboutView },
        { path: 'suggestions/:id', name: 'SuggestionDetail', component: AboutView },
      ],
    },
  ],
})

export default router
