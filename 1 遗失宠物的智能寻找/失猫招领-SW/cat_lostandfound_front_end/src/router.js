import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: () => {
      return JSON.parse(localStorage.getItem('token')) === null
        ? { name: 'login' }
        : { name: 'result' }
    },
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('./pages/Login.vue'),
  },
  {
    path: '/join',
    name: 'join',
    component: () => import('./pages/Join.vue'),
  },
  {
    path: '/home',
    name: 'home',
    component: () => import('./pages/Home.vue'),
    children: [
      {
        path: 'result',
        name: 'result',
        props: true,
        component: () => import('./pages/Result.vue'),
      },
      {
        path: 'profile',
        name: 'profile',
        component: () => import('./pages/Profile.vue'),
      },
    ],
  },
  {
    path: '/search',
    name: 'search',
    component: () => import('./pages/Search.vue'),
  },
  {
    path: '/post',
    name: 'post',
    component: () => import('./pages/Post.vue'),
  },
  {
    path: '/recommend',
    name: 'recommend',
    props: true,
    component: () => import('./pages/Recommend.vue'),
  },
  {
    path: '/detail/:post_id',
    name: 'detail',
    props: true,
    component: () => import('./pages/Detail.vue'),
  },
  {
    path: '/my-post',
    name: 'my-post',
    component: () => import('./pages/MyPost.vue'),
  },
]

export default new VueRouter({ routes })
