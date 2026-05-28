import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/news',
      name: 'news',
      component: () => import('../views/NewsView.vue'),
    },
    {
      path: '/help',
      name: 'help',
      component: () => import('../views/HelpView.vue'),
    },
    


    {
      path: '/gt3-pro',
      name: 'GT3pro',
      component: () => import('../views/categories/GT3proView.vue'),
    },
    {
      path: '/gt3-am',
      name: 'GT3am',
      component: () => import('../views/categories/GT3amView.vue'),
    },
    {
      path: '/porsche-cup',
      name: 'porsche-cup',
      component: () => import('../views/categories/PcupView.vue'),
    },
    {
      path: '/endurance',
      name: 'endurance',
      component: () => import('../views/categories/EnduranceView.vue'),
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('../views/NotFoundView.vue'),
    },
  ],
})

export default router
