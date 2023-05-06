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
      meta: { requiresAuth: true, requiredRoleLevel: 5 },
      component: () => import('../views/RegisterView.vue')
    },
    {
      path: '/cards',
      name: 'cards',
      meta: { requiresAuth: true, requiredRoleLevel: 5 },
      component: () => import('../views/CardsView.vue')
    },
    {
      path: '/schedule',
      name: 'schedule',
      meta: { requiresAuth: true, requiredRoleLevel: 2 },
      component: () => import('../views/ScheduleView.vue')
    },
    {
      path: '/admin',
      name: 'admin',
      meta: { requiresAuth: true, requiredRoleLevel: 5 },
      component: () => import('../views/AdminView.vue')
    },
    {
      path: '/log_dump',
      name: 'log_dump',
      meta: { requiresAuth: true, requiredRoleLevel: 5 },
      component: () => import('../views/LogDumpView.vue')
    },
  ]
});

export default router;
router.beforeEach(async (to, from, next) =>
{
  let access_token = localStorage.getItem('access_token');
  let role_level_raw = localStorage.getItem('role_level');
  const isAuthenticated = access_token != null;

  const requiredRoleLevel = (typeof to.meta.requiredRoleLevel === 'number') ? to.meta.requiredRoleLevel : 0;
  const currentRoleLevel = role_level_raw !== null && role_level_raw !== undefined ? parseInt(role_level_raw, 10) : 0;

  if (to.meta.requiresAuth && !isAuthenticated) next('/');
  else if (to.meta.requiresAuth && isAuthenticated && (currentRoleLevel >= requiredRoleLevel))
  {
    const header = {
      headers: {
        'Authorization': 'Bearer ' + localStorage.getItem('access_token')
      }
    };

    const resp = await axios.post('http://127.0.0.1:5000/is_authenticated/' + access_token, {}, header)
    .then((response) =>
    {
      if (response.data.status == 'success' && response.data.role_level == currentRoleLevel) next();
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
  else
  {
    if (currentRoleLevel >= requiredRoleLevel ) next();
    else next('/');
  }
});