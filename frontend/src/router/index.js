import { createRouter, createWebHistory } from 'vue-router'
import Navigation from '../components/Navigation.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Navigation
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue')
    },
  {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
  }]
})

export default router