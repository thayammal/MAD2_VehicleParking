import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import UserSummary from '@/views/UserSummary.vue';

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/test',
    name: 'testPage',
    component: () => import('../views/TestView.vue'),
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/LoginView.vue'),
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('../views/RegisterView.vue'),
  },
  {
    path: '/admin-dashboard',
    name: 'adminDashboard',
    component: () => import('../views/AdminDashboard.vue'),
  },
  {
    path: '/admin-summary',
    name: 'adminsummary',
    component: () => import('../views/AdminSummary.vue'),
//    meta: { requiresAuth: true, allowedRoles: ['admin'] },
  },
  {
    path: '/add-lot',
    name: 'parkingLots',  
    component: () => import('../views/AddparkingLot.vue'),
  },
  {
    path: '/edit-lot/:id',
    name: 'EditLot',
    component: () => import('../views/EditparkingLot.vue'),
    props: true, // Allows passing the id as a prop to the component
  },
  {
    path: '/user-stat',
    name: 'UserStat',
    component: () => import('../views/UserStat.vue'),
    meta: { requiresAuth: true, allowedRoles: ['admin'] }
  },
     {
    path: '/search',
    name: 'search',
    component: () => import('../views/SearchView.vue'),
    meta: { requiresAuth: true, allowedRoles: ['admin'] }
  },

  {
    path: '/user-dashboard',
    name: 'userDashboard',
    component: () => import('../views/UserDashboard.vue'),
    meta: { requiresAuth: true , allowedRoles: ['user']}
  },
  {
    path: '/edituser',
    name: 'editUser',
    component: () => import('../views/EditUser.vue'),
    meta: { requiresAuth: true, allowedRoles: ['user'] }  
  },
  {
    path : '/book-spot',
    name : 'bookspot',
    component: () => import('../views/BookSpot.vue')
  },
  {
  path: '/editspot/:lotId/:spotNum',
  name: 'editspot',
  component: () => import('../views/EditSpot.vue'),
  },

  {
  path: '/release-spot/',
  name: 'ReleaseSpot',
  component: () => import('@/views/ReleaseSpot.vue')
  },
  {
    path:'/user-summary',
    name: UserSummary,
    component: () => import('@/views/UserSummary.vue')
  }

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to) => {
  const token = localStorage.getItem('auth_token');
  const user = JSON.parse(localStorage.getItem('user') || '{}');
  const isAuthenticated = !!token;

  if (to.meta.requiresAuth) {
    if (!isAuthenticated) return { name: 'login' };
    if (to.meta.allowedRoles && !to.meta.allowedRoles.includes(user.role)) {
      return { name: 'home' };
    }
  }

  return true; // allow navigation if everything is fine
});


export default router
