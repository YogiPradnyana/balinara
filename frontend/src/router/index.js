import About from '@/pages/About.vue'
import Destination from '@/pages/Destination.vue'
import DetailDestination from '@/pages/DetailDestination.vue'
import Home from '@/pages/Home.vue'
import Suggest from '@/pages/Profile/Suggest.vue'
import Wishlist from '@/pages/Profile/Wishlist.vue'
import SuggestSpot from '@/pages/SuggestSpot.vue'
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

    // User Profile
    {
      path: '/profile',
      children: [
        { path: '', name: 'Profile', component: About },
        { path: 'wishlist', name: 'Wishlist', component: Wishlist },
        { path: 'reviews', name: 'UserReview', component: About },
        { path: 'suggestions', name: 'UserSuggestion', component: Suggest },
        { path: 'suggestions/:id', name: 'SuggestionDetail', component: About },
      ],
    },
  ],
})

export default router
