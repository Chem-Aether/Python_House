<template>
  <el-container style="height:100vh">
    <el-aside width="200px">
      <el-menu default-active="1" router>
        <el-menu-item index="/admin/home">首页</el-menu-item>
        <el-menu-item index="/admin/user">用户管理</el-menu-item>
        <el-menu-item index="/admin/city">房价管理</el-menu-item>
        <el-menu-item index="/admin/news">资讯管理</el-menu-item>
        <el-menu-item index="/admin/sysconfig">系统配置</el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header style="background:#fff">管理员后台</el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
// admin layout
</script>
