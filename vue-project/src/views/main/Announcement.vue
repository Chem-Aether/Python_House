<template>
  <div class="announcement-page">
    <!-- 页面标题 + 搜索框 -->
    <div class="page-header">
      <h2>公告信息管理</h2>
      <el-input
        v-model="searchTitle"
        placeholder="输入标题关键词搜索"
        clearable
        @keyup.enter="handleSearch"
        class="search-input"
      >
        <template #suffix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>
    </div>

    <div class="main-container">
      <!-- 右侧分类筛选栏 -->
      <div class="category-sidebar">
        <div class="sidebar-title">资讯分类</div>
        <!-- 移除 el-button-group，改用普通 div 容器 -->
        <div class="category-list">
            <el-button 
            :class="{ active: activeCategory === '全部' }"
            @click="handleCategoryChange('全部')"
            size="large"
            type="primary"
            plain
            class="all-btn category-btn"
            >
            全部
            </el-button>
            <el-button 
            v-for="category in categoryList" 
            :key="category.typename"
            :class="{ active: activeCategory === category.typename }"
            @click="handleCategoryChange(category.typename)"
            size="large"
            type="primary"
            plain
            class="category-btn"
            >
            {{ category.typename }}
            </el-button>
        </div>
      </div>

      <!-- 左侧公告列表 -->
      <div class="announcement-list">
        <div v-if="loading" class="loading-tip">
          <el-skeleton :rows="6" animated />
        </div>

        <div v-else-if="newsList.length === 0" class="empty-tip">
          <el-empty description="暂无相关公告" />
        </div>

        <div v-else class="card-list">
          <div 
            v-for="item in newsList" 
            :key="item.id" 
            class="announcement-card"
          >
            <div class="card-img">
              <img 
                :src="item.picture || '/default-news.jpg'" 
                :alt="item.title"
                @error="handleImgError($event)"
              />
            </div>
            <div class="card-content">
              <div class="card-title">{{ item.title }}</div>
              <div class="card-intro">{{ item.introduction || '暂无简介' }}</div>
              <div class="card-meta">
                <span class="meta-item">
                  <el-icon><User /></el-icon> {{ item.name || '管理员' }}
                </span>
                <span class="meta-item">
                  <el-icon><Calendar /></el-icon> {{ formatTime(item.addtime) }}
                </span>
                <span class="meta-item">
                  <el-icon><View /></el-icon> {{ item.clicknum || 0 }}
                </span>
              </div>
              <div class="card-stats">
                <span class="stat-item">
                  <el-icon><svg t="1774005084870" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="1682" width="200" height="200"><path d="M832 364.8h-147.2s19.2-64 32-179.2c6.4-57.6-38.4-115.2-102.4-121.6h-12.8c-51.2 0-83.2 32-102.4 76.8l-38.4 96c-32 64-57.6 102.4-76.8 115.2-25.6 12.8-121.6 12.8-128 12.8H128c-38.4 0-64 25.6-64 57.6v480c0 32 25.6 57.6 64 57.6h646.4c96 0 121.6-64 134.4-153.6l51.2-307.2c6.4-70.4-6.4-134.4-128-134.4z m-576 537.6H128V422.4h128v480z m640-409.6l-51.2 307.2c-12.8 57.6-12.8 102.4-76.8 102.4H320V422.4c44.8 0 70.4-6.4 89.6-19.2 32-12.8 64-64 108.8-147.2 25.6-64 38.4-96 44.8-102.4 6.4-19.2 19.2-32 44.8-32h6.4c32 0 44.8 32 44.8 51.2-12.8 102.4-32 166.4-32 166.4l-25.6 83.2h243.2c19.2 0 32 0 44.8 12.8 12.8 12.8 6.4 38.4 6.4 57.6z" p-id="1683"></path></svg></el-icon> 
                  {{ item.thumbsupnum || 0 }}
                </span>
                <span class="stat-item">
                  <el-icon><svg t="1774005126773" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="2647" width="200" height="200"><path d="M161.28 671.402667c21.76 21.76 48.213333 32.426667 78.933333 32.426666h201.301334l-26.453334 102.4c-4.693333 18.346667-3.84 36.693333 2.56 54.570667 6.4 17.92 17.066667 32.853333 32.426667 43.946667l29.44 22.186666c11.946667 8.96 25.173333 12.8 40.106667 11.52 14.890667-1.28 27.690667-6.826667 37.930666-17.493333l1.28-1.28 188.074667-219.690667c5.12-5.12 9.386667-10.666667 12.373333-17.066666h62.293334c21.333333 0 39.68-8.106667 54.186666-24.746667 13.653333-14.933333 20.48-32.853333 20.48-53.76V249.173333c0-20.906667-6.826667-38.826667-20.48-53.76-14.933333-16.213333-32.853333-24.704-54.186666-24.704H315.690667c-15.786667 0-29.866667 4.266667-43.093334 12.8-13.226667 8.533333-22.613333 20.053333-28.586666 34.56L136.533333 476.501333c-5.546667 13.653333-8.533333 27.733333-8.533333 42.666667v72.490667c0 30.72 11.093333 57.173333 32.853333 78.933333l0.426667 0.853333zM768.213333 256.853333h42.666667v341.248h-42.666667V256.810667zM213.76 519.978667c0-3.413333 0.853333-6.826667 2.133333-9.813334L321.28 256.853333h361.685333v386.901334l-171.050666 200.874666-10.666667-7.68q-2.56-2.56-2.986667-4.266666c-0.426667-1.706667-0.853333-3.413333 0-5.12l53.76-208.981334H240.597333c-7.253333 0-13.653333-2.56-18.773333-7.68a24.832 24.832 0 0 1-7.68-18.346666v-72.533334h-0.426667z" p-id="2648"></path></svg></el-icon> 
                  {{ item.crazilynum || 0 }}
                </span>
                <span class="stat-item">
                  <el-icon><Star /></el-icon> {{ item.storeupnum || 0 }}
                </span>
              </div>
              <div class="card-actions">
                <el-button type="text" size="small" @click="toNewsDetail(item.id)">查看详情</el-button>
              </div>
            </div>
          </div>
        </div>

        <!-- 分页控件 -->
        <div class="pagination-wrap" v-if="!loading && newsList.length > 0">
          <el-pagination
            :current-page="currentPage"
            :page-size="pageSize"
            :page-sizes="[10, 20, 30, 40]"
            :total="totalCount"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            @prev-click="handlePrevClick"
            @next-click="handleNextClick"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>

import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { request } from '@/utils/request'
import { ElMessage } from 'element-plus'
import {User, Star, Calendar, View, Search } from '@element-plus/icons-vue'

const router = useRouter()

// 分页参数
const currentPage = ref(1)
const pageSize = ref(20)
const totalCount = ref(0)
const loading = ref(false)
const isFirstLoad = ref(true)

// 搜索与筛选参数
const searchTitle = ref('')
const activeCategory = ref('全部')
const categoryList = ref([])
const newsList = ref([])

// 请求防抖函数
let requestTimer = null
const debounceRequest = (fn, delay = 300) => {
  return (...args) => {
    if (requestTimer) clearTimeout(requestTimer)
    requestTimer = setTimeout(() => {
      fn(...args)
    }, delay)
  }
}

// 加载分类列表
const fetchCategoryList = async () => {
  try {
    const params = {
        page: 1,
        page_size: 20
      }
    const res = await request.get('/news/types/', params)
    categoryList.value = res.items || res || []
  } catch (error) {
    console.error('获取分类列表失败：', error)
    ElMessage.error('加载分类失败')
    categoryList.value = [
      { typename: '系统公告' },
      { typename: '活动通知' },
      { typename: '行业资讯' },
      { typename: '政策解读' }
    ]
  }
}

// 加载公告列表
const fetchNewsList = async (isInit = false) => {
  if (loading.value && !isInit) return
  
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      title: searchTitle.value.trim() || undefined,
      typename: activeCategory.value === '全部' ? undefined : activeCategory.value
    }

    const res = await request.get('/news/', params)
    newsList.value = res.items || res || []
    totalCount.value = res.total || newsList.value.length
  } catch (error) {
    console.error('获取公告列表失败：', error)
    ElMessage.error('加载公告失败，请稍后重试')
    newsList.value = []
    totalCount.value = 0
  } finally {
    loading.value = false
    if (isInit) isFirstLoad.value = false
  }
}

// 防抖后的请求函数
const debouncedFetchNewsList = debounceRequest(fetchNewsList)

// 搜索按钮点击
const handleSearch = () => {
  currentPage.value = 1
  debouncedFetchNewsList()
}

// 分类切换
const handleCategoryChange = (category) => {
  if (activeCategory.value === category) return
  activeCategory.value = category
  currentPage.value = 1
  debouncedFetchNewsList()
}

// 分页事件处理
const handleSizeChange = (val) => {
  if (pageSize.value === val) return
  pageSize.value = val
  currentPage.value = 1
  debouncedFetchNewsList()
}

const handleCurrentChange = (val) => {
  if (currentPage.value === val) return
  currentPage.value = val
  debouncedFetchNewsList()
}

const handlePrevClick = () => {
  if (currentPage.value <= 1) return
  currentPage.value -= 1
  debouncedFetchNewsList()
}

const handleNextClick = () => {
  const maxPage = Math.ceil(totalCount.value / pageSize.value)
  if (currentPage.value >= maxPage) return
  currentPage.value += 1
  debouncedFetchNewsList()
}

// 图片加载失败处理
const handleImgError = (e) => {

}

// 时间格式化
const formatTime = (timeStr) => {
  if (!timeStr) return ''
  const date = new Date(timeStr)
  return `${date.getFullYear()}-${(date.getMonth()+1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')}`
}

// 跳转到详情页
const toNewsDetail = (id) => {
  router.push({
    path: '/home/newsDetail',
    query: { id }
  })
}

// 初始化加载
onMounted(async () => {
  await fetchCategoryList()
  fetchNewsList(true)
})

// 核心修复3：清理定时器（现在 onUnmounted 已导入）
onUnmounted(() => {
  if (requestTimer) clearTimeout(requestTimer)
})
</script>

<style scoped>
.announcement-page {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  border-bottom: 1px solid #eee;
  padding-bottom: 15px;
}

.page-header h2 {
  font-size: 22px;
  font-weight: 600;
  margin: 0;
  color: #333;
}

.search-input {
  width: 300px;
}

.main-container {
  display: flex;
  gap: 30px;
}

/* 修复左侧分类栏样式 - 移除按钮组 */
.category-sidebar {
  width: 220px;
  flex-shrink: 0;
  background: #fff;
  border-radius: 8px;
  padding: 0;
}

.sidebar-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 15px;
  color: #333;
  padding-left: 8px;
  border-left: 3px solid #409eff;
  line-height: 1.4;
}

/* 分类列表容器 - 普通div，不是按钮组 */
.category-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 12px;
  width: 100%;
}

/* 统一的按钮样式 - 完全独立的按钮，边框不会被遮挡 */
.category-btn {
  width: 100%;
  justify-content: center;
  margin: 0 !important;
  height: 40px;
  font-size: 14px;
  border-radius: 6px;
  transition: all 0.3s;
  border: 1px solid #dcdfe6;
  background-color: #fff;
  color: #606266;
}

/* 全部按钮单独样式 */
.all-btn {
  margin-top: 8px !important;
}

/* 按钮激活状态 */
.category-btn.active {
  background-color: #409eff;
  color: #fff;
  border-color: #409eff;
  font-weight: 500;
}

/* 按钮悬浮效果 */
.category-btn:hover:not(.active) {
  background-color: #ecf5ff;
  border-color: #409eff;
  color: #409eff;
  transform: translateX(2px);
}

/* 移除 Element Plus 按钮组可能带来的影响 */
:deep(.el-button-group) {
  display: none;
}

.announcement-list {
  flex: 1;
  min-width: 0;
}

.loading-tip {
  padding: 40px 0;
}

.empty-tip {
  padding: 60px 0;
  text-align: center;
}

.card-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(500px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.announcement-card {
  display: flex;
  gap: 15px;
  padding: 15px;
  border: 1px solid #eee;
  border-radius: 8px;
  transition: all 0.3s;
  cursor: pointer;
  background: #fff;
}

.announcement-card:hover {
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  border-color: #409eff;
  transform: translateY(-2px);
}

.card-img {
  width: 120px;
  height: 80px;
  flex-shrink: 0;
  border-radius: 4px;
  overflow: hidden;
  background: #f5f5f5;
}

.card-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.card-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
  min-width: 0;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.card-intro {
  font-size: 14px;
  color: #666;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  flex: 1;
}

.card-meta {
  display: flex;
  gap: 15px;
  font-size: 12px;
  color: #999;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.card-stats {
  display: flex;
  gap: 15px;
  font-size: 12px;
  color: #666;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.card-actions {
  margin-top: 5px;
}

.pagination-wrap {
  display: flex;
  justify-content: center;
  margin-top: 30px;
}

/* 响应式布局优化 */
@media (max-width: 1200px) {
  .card-list {
    grid-template-columns: repeat(auto-fill, minmax(450px, 1fr));
  }
}

@media (max-width: 992px) {
  .main-container {
    gap: 20px;
  }
  
  .category-sidebar {
    width: 200px;
  }
  
  .card-list {
    grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  }
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }
  
  .search-input {
    width: 100%;
  }
  
  .main-container {
    flex-direction: column;
  }

  .category-sidebar {
    width: 100%;
    margin-bottom: 20px;
  }

  /* 移动端改为横向滚动布局 */
  .category-list {
    flex-direction: row;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 15px;
  }

  .category-btn {
    width: auto;
    min-width: 80px;
    padding: 0 16px;
    flex-shrink: 0;
  }

  .all-btn {
    width: auto;
    min-width: 80px;
    margin-top: 0 !important;
  }
  
  .card-list {
    grid-template-columns: 1fr;
  }
  
  .announcement-card {
    padding: 12px;
  }
  
  .card-img {
    width: 100px;
    height: 70px;
  }
}

/* 针对小屏手机的进一步优化 */
@media (max-width: 480px) {
  .announcement-card {
    flex-direction: column;
  }
  
  .card-img {
    width: 100%;
    height: 160px;
  }
  
  .card-meta, .card-stats {
    flex-wrap: wrap;
    gap: 10px;
  }
}
</style>