<template>
  <el-container style="height:100vh">
    <el-aside width="200px">
      <el-menu default-active="1" router>
        <el-menu-item index="/user/home">首页</el-menu-item>
        <el-menu-item index="/user/house">房源</el-menu-item>
        <el-menu-item index="/user/news">资讯</el-menu-item>
        <el-menu-item index="/user/collect">收藏</el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header style="background:#fff">用户面板</el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
// user layout with left menu
</script>
