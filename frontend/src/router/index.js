import About from '@/pages/About.vue'
import Home from '@/pages/Home.vue'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // Public
    {
      path: '/',
      name: 'Home',
      component: Home,
    },
    {
      path: '/destinations',
      name: 'Destinations',
      component: About,
    },
    {
      path: '/destinations/:id',
      name: 'DetailDestinations',
      component: About,
      props: true,
    },
    {
      path: '/suggest',
      name: 'Suggest',
      component: About,
    },
    {
      path: '/review',
      name: 'Review',
      component: About,
    },
    {
      path: '/about',
      name: 'About',
      component: About,
    },

    // User Profile
    {
      path: '/profile',
      component: About,
      children: [
        { path: '', name: 'Profile', component: About },
        { path: 'wishlist', name: 'Wishlist', component: About },
        { path: 'reviews', name: 'UserReviews', component: About },
        { path: 'suggestions', name: 'UserSuggestions', component: About },
        { path: 'suggestions/:id', name: 'SuggestionDetail', component: About },
      ],
    },
  ],
})

export default router
