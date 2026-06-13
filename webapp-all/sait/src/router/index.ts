import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { title: 'Главная' }
    },
    {
      path: '/news',
      name: 'news',
      component: () => import('../views/NewsView.vue'),
      meta: { title: 'Новости' }
    },
    {
      path: '/new/:id',
      name: 'new',
      // @ts-ignore
      component: () => import('../views/NewView.vue'),
    },
    {
      path: '/form/:id',
      name: 'form',
      // @ts-ignore
      component: () => import('../views/FormView.vue'),
    },
    {
      path: '/help',
      name: 'help',
      component: () => import('../views/HelpView.vue'),
      meta: { title: 'Помощь' }
    },
    {
      path: '/dc',
      name: 'discord',
      // @ts-ignore
      component: () => import('../views/DcView.vue'),
      meta: { title: 'Дискорд ссылка' }
    },
    {
      path: '/event-week',
      name: 'EventWeek',
      // @ts-ignore
      component: () => import('../views/EventWeekView.vue'),
      meta: { title: 'Недельный ивент' }
    },
    {
      path: '/setups',
      name: 'setups',
      // @ts-ignore
      component: () => import('../views/SetupsView.vue'),
      meta: { title: 'Car setups' }
    },



    {
      path: '/gt3-pro',
      name: 'GT3pro',
      component: () => import('../views/categories/GT3proView.vue'),
      meta: { title: 'GT3 Pro' }
    },
    {
      path: '/gt3-am',
      name: 'GT3am',
      // @ts-ignore
      component: () => import('../views/categories/GT3amView.vue'),
      meta: { title: 'GT3 am' }
    },
    {
      path: '/porsche-cup',
      name: 'porsche-cup',
      component: () => import('../views/categories/PcupView.vue'),
      meta: { title: 'Porsche Cup' }
    },
    {
      path: '/endurance',
      name: 'endurance',
      component: () => import('../views/categories/EnduranceView.vue'),
      meta: { title: 'Endurance' }
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('../views/NotFoundView.vue'),
      meta: { title: '404' }
    },
  ],
})

export default router
