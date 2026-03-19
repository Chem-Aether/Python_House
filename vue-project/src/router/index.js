import { createRouter, createWebHistory } from 'vue-router'


// 定义路由
const routes = [
  { path: '/login', component: () => import('@/views/Login.vue') },
  { path: '/register', component: () => import('@/views/Register.vue') },
  {
    path: '/user',
    component: () => import('@/views/user/Layout.vue'),
    children: [
      { path: 'home', component: () => import('@/views/user/UserHome.vue') },
      { path: 'house', component: () => import('@/views/user/House.vue') },
      { path: 'news', component: () => import('@/views/user/News.vue') },
      { path: 'collect', component: () => import('@/views/user/Collect.vue') },
    ]
  },
  {
    path: '/admin',
    component: () => import('@/views/admin/Layout.vue'),
    children: [
      { path: 'home', component: () => import('@/views/admin/AdminHome.vue') },
      { path: 'user', component: () => import('@/views/admin/UserManage.vue') },
      { path: 'city', component: () => import('@/views/admin/City.vue') },
      { path: 'news', component: () => import('@/views/admin/News.vue') },
      { path: 'sysconfig', component: () => import('@/views/admin/Sysconfig.vue') },
    ]
  }
];



// 创建路由实例
const router = createRouter({
  history: createWebHistory(), // 使用 HTML5 历史模式
  routes, // 路由配置
});


export default router;
