import axios from 'axios';
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes:
  [
    {
      path: '/login',
      redirect: '/'
    },
    {
      path: '/',
      name: 'home',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/register',
      name: 'register',
      meta: { requiresAuth: true },
      component: () => import('../views/RegisterView.vue')
    },
    {
      path: '/cards',
      name: 'cards',
      meta: { requiresAuth: true },
      component: () => import('../views/CardsView.vue')
    },
    {
      path: '/schedule',
      name: 'schedule',
      meta: { requiresAuth: true },
      component: () => import('../views/ScheduleView.vue')
    },
    {
      path: '/admin',
      name: 'admin',
      meta: { requiresAuth: true },
      component: () => import('../views/AdminView.vue')
    }
  ]
});

export default router;
router.beforeEach(async (to, from, next) =>
{
  let access_token = localStorage.getItem('access_token');
  const isAuthenticated = access_token != null;

  if (to.meta.requiresAuth && !isAuthenticated) next('/');
  else if (to.meta.requiresAuth && isAuthenticated)
  {
    const header = {
      headers: {
        'Authorization': 'Bearer ' + localStorage.getItem('access_token')
      }
    };

    const resp = await axios.post('http://127.0.0.1:5000/is_authenticated/' + access_token, {}, header)
    .then((response) =>
    {
      if (response.data.status == 'success') next();
      else
      {
        location.reload();
        localStorage.removeItem('access_token');
        next('/');
      }
    })
    .catch((error) =>
    {
      location.reload();
      localStorage.removeItem('access_token');
      next('/');
    });
  }
  else next();
});