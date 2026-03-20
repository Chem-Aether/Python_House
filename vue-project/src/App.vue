<template>
  <div id="app">
    <!-- 移除所有包裹 router-view 的固定高度/overflow 样式 -->
    <router-view />
  </div>
</template>

<style>
/* 核心修复：确保根容器允许滚动 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
html, body {
  height: auto; /* 必须是 auto，不能是 100% */
  overflow-y: auto; /* 允许垂直滚动 */
}
#app {
  min-height: 100vh; /* 占满视口，但允许超出 */
  width: 100%;
  overflow-y: auto; /* 关键：允许 app 容器滚动 */
}
</style>