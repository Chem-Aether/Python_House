<template>
  <div class="news-detail-page">
    <!-- 加载状态 -->
    <div v-if="loading" class="loading-container">
      <el-skeleton 
        :animated="true" 
        :rows="8" 
        width="100%" 
        class="skeleton-card"
      />
    </div>

    <!-- 空状态/加载失败 -->
    <div v-else-if="!newsData" class="empty-container">
      <el-empty description="暂无新闻内容" />
      <el-button type="primary" @click="goBack" class="back-btn">返回列表</el-button>
    </div>

    <!-- 新闻详情内容 -->
    <div v-else class="news-content">
      <!-- 标题区域 -->
      <div class="news-header">
        <h1 class="news-title">{{ newsData.title }}</h1>
        <div class="news-meta">
          <span class="meta-item">
            <el-icon><User /></el-icon>
            {{ newsData.name || '管理员' }}
          </span>
          <span class="meta-item">
            <el-icon><Calendar /></el-icon>
            {{ formatTime(newsData.addtime) }}
          </span>
          <span class="meta-item">
            <el-icon><View /></el-icon>
            {{ newsData.clicknum || 0 }} 阅读
          </span>
        </div>
      </div>

      <!-- 分割线 -->
      <div class="divider"></div>

      <!-- 正文区域 -->
      <div class="news-body">
        <!-- 封面图 -->
        <div v-if="newsData.picture" class="news-cover">
          <img 
            :src="newsData.picture" 
            :alt="newsData.title"
            @error="handleImgError"
            loading="lazy"
          />
        </div>

        <!-- 内容正文（分行显示简介和正文） -->
        <div class="news-text">
          <!-- 简介区域 -->
          <div v-if="newsData.introduction" class="news-intro">
            <span class="intro-label">简介：</span>
            {{ newsData.introduction }}
          </div>
          <!-- 正文区域 -->
          <div v-if="newsData.content" class="news-main-content">
            <span class="content-label">正文：</span>
            {{ newsData.content }}
          </div>
          <!-- 空状态 -->
          <div v-if="!newsData.introduction && !newsData.content" class="empty-content">
            暂无详细内容
          </div>
        </div>
      </div>

      <!-- 互动数据 -->
      <div class="news-stats">
        <div class="stat-item">
          <el-icon><svg t="1774005084870" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="1682" width="200" height="200"><path d="M832 364.8h-147.2s19.2-64 32-179.2c6.4-57.6-38.4-115.2-102.4-121.6h-12.8c-51.2 0-83.2 32-102.4 76.8l-38.4 96c-32 64-57.6 102.4-76.8 115.2-25.6 12.8-121.6 12.8-128 12.8H128c-38.4 0-64 25.6-64 57.6v480c0 32 25.6 57.6 64 57.6h646.4c96 0 121.6-64 134.4-153.6l51.2-307.2c6.4-70.4-6.4-134.4-128-134.4z m-576 537.6H128V422.4h128v480z m640-409.6l-51.2 307.2c-12.8 57.6-12.8 102.4-76.8 102.4H320V422.4c44.8 0 70.4-6.4 89.6-19.2 32-12.8 64-64 108.8-147.2 25.6-64 38.4-96 44.8-102.4 6.4-19.2 19.2-32 44.8-32h6.4c32 0 44.8 32 44.8 51.2-12.8 102.4-32 166.4-32 166.4l-25.6 83.2h243.2c19.2 0 32 0 44.8 12.8 12.8 12.8 6.4 38.4 6.4 57.6z" p-id="1683"></path></svg></el-icon>
          <span>{{ newsData.thumbsupnum || 0 }} 点赞</span>
        </div>
        <div class="stat-item">
          <el-icon><svg t="1774005126773" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="2647" width="200" height="200"><path d="M161.28 671.402667c21.76 21.76 48.213333 32.426667 78.933333 32.426666h201.301334l-26.453334 102.4c-4.693333 18.346667-3.84 36.693333 2.56 54.570667 6.4 17.92 17.066667 32.853333 32.426667 43.946667l29.44 22.186666c11.946667 8.96 25.173333 12.8 40.106667 11.52 14.890667-1.28 27.690667-6.826667 37.930666-17.493333l1.28-1.28 188.074667-219.690667c5.12-5.12 9.386667-10.666667 12.373333-17.066666h62.293334c21.333333 0 39.68-8.106667 54.186666-24.746667 13.653333-14.933333 20.48-32.853333 20.48-53.76V249.173333c0-20.906667-6.826667-38.826667-20.48-53.76-14.933333-16.213333-32.853333-24.704-54.186666-24.704H315.690667c-15.786667 0-29.866667 4.266667-43.093334 12.8-13.226667 8.533333-22.613333 20.053333-28.586666 34.56L136.533333 476.501333c-5.546667 13.653333-8.533333 27.733333-8.533333 42.666667v72.490667c0 30.72 11.093333 57.173333 32.853333 78.933333l0.426667 0.853333zM768.213333 256.853333h42.666667v341.248h-42.666667V256.810667zM213.76 519.978667c0-3.413333 0.853333-6.826667 2.133333-9.813334L321.28 256.853333h361.685333v386.901334l-171.050666 200.874666-10.666667-7.68q-2.56-2.56-2.986667-4.266666c-0.426667-1.706667-0.853333-3.413333 0-5.12l53.76-208.981334H240.597333c-7.253333 0-13.653333-2.56-18.773333-7.68a24.832 24.832 0 0 1-7.68-18.346666v-72.533334h-0.426667z" p-id="2648"></path></svg></el-icon>
          <span>{{ newsData.crazilynum || 0 }} 踩</span>
        </div>
        <div class="stat-item">
          <el-icon><Star /></el-icon>
          <span>{{ newsData.storeupnum || 0 }} 收藏</span>
        </div>
      </div>

      <!-- 返回按钮 -->
      <div class="action-buttons">
        <el-button type="primary" @click="goBack">返回列表</el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { request } from '@/utils/request'
import { ElMessage } from 'element-plus'
import { User, Calendar, View, Star } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()

// 响应式数据
const loading = ref(true)
const newsData = ref(null)

// 获取新闻ID（从路由参数中）
const newsId = route.query.id

// 时间格式化
const formatTime = (timeStr) => {
  if (!timeStr) return ''
  const date = new Date(timeStr)
  if (isNaN(date.getTime())) return ''
  return `${date.getFullYear()}-${(date.getMonth()+1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')} ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`
}

// 图片加载失败处理
const handleImgError = (e) => {
  e.target.src = 'https://picsum.photos/800/450' // 占位图
}

// 返回列表页
const goBack = () => {
  router.push('/home/announcement') // 跳回公告列表页
}

// 获取新闻详情
const fetchNewsDetail = async () => {
  if (!newsId) {
    ElMessage.warning('无效的新闻ID')
    loading.value = false
    return
  }

  try {
    // 接口地址：http://localhost:8000/news/[新闻ID]
    const res = await request.get(`/news/${newsId}`)
    newsData.value = res.data || res // 适配不同的接口返回格式
  } catch (error) {
    console.error('获取新闻详情失败：', error)
    ElMessage.error('加载新闻详情失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

// 初始化加载
onMounted(() => {
  fetchNewsDetail()
})
</script>

<style scoped>
/* 页面整体样式 */
.news-detail-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
  min-height: 100vh;
  background-color: #f8f9fa;
}

/* 加载状态 */
.loading-container {
  display: flex;
  justify-content: center;
  padding: 40px 0;
}

.skeleton-card {
  max-width: 800px;
  width: 100%;
}

/* 空状态 */
.empty-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 0;
}

.back-btn {
  margin-top: 20px;
}

/* 新闻内容容器 */
.news-content {
  max-width: 800px;
  margin: 0 auto;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.05);
  padding: 40px;
}

/* 新闻标题区域 */
.news-header {
  margin-bottom: 30px;
  text-align: center;
}

.news-title {
  font-size: 28px;
  font-weight: 700;
  color: #1f2937;
  line-height: 1.4;
  margin: 0 0 20px 0;
}

.news-meta {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 24px;
  font-size: 14px;
  color: #6b7280;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

/* 分割线 */
.divider {
  height: 1px;
  background-color: #e5e7eb;
  margin: 20px 0 30px 0;
}

/* 新闻正文区域 */
.news-body {
  margin-bottom: 40px;
}

/* 封面图 */
.news-cover {
  margin-bottom: 30px;
  border-radius: 8px;
  overflow: hidden;
}

.news-cover img {
  width: 100%;
  height: auto;
  object-fit: cover;
  display: block;
}

/* 正文文本容器 */
.news-text {
  text-align: left;
  white-space: pre-wrap; /* 保留换行和空格 */
  word-break: break-word;
}

/* 简介样式 */
.news-intro {
  font-size: 16px;
  line-height: 1.8;
  color: #4b5563;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px dashed #e5e7eb;
}

.intro-label {
  font-weight: 600;
  color: #1f2937;
}

/* 正文样式 */
.news-main-content {
  font-size: 16px;
  line-height: 1.8;
  color: #374151;
}

.content-label {
  font-weight: 600;
  color: #1f2937;
}

/* 空内容样式 */
.empty-content {
  font-size: 16px;
  color: #9ca3af;
  text-align: center;
  padding: 20px 0;
}

/* 互动数据 */
.news-stats {
  display: flex;
  justify-content: center;
  gap: 30px;
  padding: 20px 0;
  border-top: 1px solid #f3f4f6;
  margin-bottom: 30px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: #4b5563;
}

/* 操作按钮 */
.action-buttons {
  display: flex;
  justify-content: center;
}

.action-buttons .el-button {
  padding: 10px 30px;
  border-radius: 8px;
  font-size: 16px;
}

/* 响应式适配 */
@media (max-width: 768px) {
  .news-detail-page {
    padding: 20px 15px;
  }

  .news-content {
    padding: 25px 20px;
  }

  .news-title {
    font-size: 22px;
  }

  .news-meta {
    flex-wrap: wrap;
    gap: 12px;
  }

  .news-intro, .news-main-content {
    font-size: 15px;
    line-height: 1.7;
  }

  .news-stats {
    gap: 20px;
  }
}

@media (max-width: 480px) {
  .news-title {
    font-size: 18px;
  }

  .news-stats {
    flex-direction: column;
    gap: 15px;
    align-items: center;
  }
}
</style>