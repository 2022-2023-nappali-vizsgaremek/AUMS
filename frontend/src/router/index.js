import { createRouter, createWebHistory } from 'vue-router'
import Navigation from '../components/Navigation.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
    path: '/login',
    name: 'login',
    component: () => import('../views/LoginView.vue')
    },
    {
      path: '/',
      name: 'home',
      component: () => import('../views/LoginView.vue')
    },
    {
    path: '/register',
    name: 'register',
    component: () => import('../views/RegisterView.vue')
    }]
})

export default router