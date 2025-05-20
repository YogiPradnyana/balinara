import About from '@/pages/About.vue'
import Destination from '@/pages/Destination.vue'
import DetailDestination from '@/pages/DetailDestination.vue'
import DetailSuggest from '@/pages/DetailSuggest.vue'
import Home from '@/pages/Home.vue'
import Profile from '@/pages/Profile/Profile.vue'
import Suggest from '@/pages/Profile/Suggest.vue'
import Wishlist from '@/pages/Profile/Wishlist.vue'
import Search from '@/pages/Search.vue'
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
    {
      path: '/search',
      name: 'Search',
      component: Search,
    },

    // User Profile
    {
      path: '/user',
      children: [
        { path: 'profile', name: 'Profile', component: Profile },
        { path: 'wishlist', name: 'Wishlist', component: Wishlist },
        { path: 'reviews', name: 'UserReview', component: About },
        { path: 'suggestions', name: 'UserSuggestion', component: Suggest },
        { path: 'suggestions/:id', name: 'SuggestionDetail', component: DetailSuggest },
      ],
    },
  ],
})

export default router
