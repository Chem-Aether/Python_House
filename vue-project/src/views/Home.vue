<template>
  <div class="home-layout">
    <!-- 顶部导航：常驻显示 -->
    <header class="header">
      <div class="header-container">
        <div class="logo">二手房信息系统</div>
        <nav class="nav">
          <!-- 导航按钮：指向子路由 -->
          <router-link 
            to="/home/main" 
            class="nav-item"
            :class="{ active: $route.path === '/home/main' }"
          >
            <i class="el-icon-house"></i> 首页
          </router-link>
          <router-link 
            to="/home/secondhand" 
            class="nav-item"
            :class="{ active: $route.path === '/home/secondhand' }"
          >
            <i class="el-icon-office-building"></i> 二手房价
          </router-link>
          <router-link 
            to="/home/announcement" 
            class="nav-item"
            :class="{ active: $route.path === '/home/announcement' }"
          >
            <i class="el-icon-bell"></i> 公告信息
          </router-link>
        </nav>
        <div class="header-right">
          <router-link to="/login" class="login-btn">登录/注册</router-link>
        </div>
      </div>
    </header>

    <!-- 子路由内容区：渲染 main/secondhand/announcement -->
    <div class="content-container">
      <router-view />
    </div>
  </div>
</template>

<style scoped>
/* 布局样式 */
.home-layout {
  width: 100%;
  min-height: 100vh;
  background-color: #f8f9fa;
}

/* 顶部导航样式 */
.header {
  background: #fff;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  padding: 0 20px;
  position: sticky; /* 吸顶效果 */
  top: 0;
  z-index: 999;
}
.header-container {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  height: 70px;
  justify-content: space-between;
}
.logo {
  font-size: 22px;
  font-weight: 600;
  color: #333;
}
.nav {
  display: flex;
  gap: 30px;
}
.nav-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px;
  color: #666;
  text-decoration: none;
  border-radius: 4px;
  transition: all 0.3s;
}
.nav-item.active,
.nav-item:hover {
  background: #409eff;
  color: #fff;
}
.header-right {
  display: flex;
  align-items: center;
}
.login-btn {
  background: #f56c6c;
  color: #fff;
  padding: 8px 16px;
  border-radius: 4px;
  text-decoration: none;
  font-size: 14px;
}

/* 子路由内容容器 */
.content-container {
  width: 100%;
  min-height: calc(100vh - 70px); /* 减去导航高度 */
  padding: 0;
}
</style>