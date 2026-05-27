import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'servers',
      component: HomeView,
    },
    {
      path: '/server/:ip',
      name: 'server-details',
      component: () => import('../views/ServerDetailsView.vue'),
      props: true,
    },
  ],
})

export default router
