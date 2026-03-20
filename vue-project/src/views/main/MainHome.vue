<template>
  <div class="main-home">
    <!-- 大屏轮播图（静态） -->
    <section class="carousel-section">
      <el-carousel height="500px" :interval="2000">
        <el-carousel-item v-for="(item, index) in carouselList" :key="index">
          <img :src="item.image" :alt="`轮播图${index+1}`" class="carousel-img" />
        </el-carousel-item>
      </el-carousel>
    </section>

    <!-- 主体内容区 -->
    <main class="main-container">
      <div class="content-wrapper">
        <!-- 左侧：公告列表 + 房屋列表 -->
        <div class="left-content">
          <!-- 公告列表 -->
          <div class="announcement-box">
            <div class="box-title">
              <h3>最新公告</h3>
              <router-link to="/home/announcement" class="more-link">更多 ></router-link>
            </div>
            <!-- 加载中 -->
            <div v-if="loading" class="loading">加载中...</div>
            <!-- 无数据 -->
            <div v-else-if="announcementList.length === 0" class="empty">暂无公告数据</div>
            <!-- 公告列表 -->
            <ul v-else class="announcement-list">
              <li v-for="(item, index) in announcementList" :key="item.id" class="announcement-item" @click="toNewsDetail(item.id)">
                <span class="badge new" v-if="index < 3">新</span>
                <span class="title">{{ item.title }}</span>
                <span class="date">{{ item.create_time }}</span>
              </li>
            </ul>
          </div>

          <!-- 房屋列表 -->
          <div class="house-list-box">
            <div class="box-title">
              <h3>精选房源</h3>
              <router-link to="/home/secondhand" class="more-link">查看全部 ></router-link>
            </div>
            <!-- 加载中 -->
            <div v-if="houseLoading" class="loading">加载中...</div>
            <!-- 无数据 -->
            <div v-else-if="houseList.length === 0" class="empty">暂无房源数据</div>
            <!-- 房源列表 -->
            <div v-else class="house-grid">
              <div v-for="(house, index) in houseList" :key="house.id" class="house-card">
                <div class="house-img">
                  <img :src="house.picture" :alt="house.title" />
                  <span class="tag">{{ house.usetype }}</span>
                </div>
                <div class="house-info">
                  <h4 class="house-title">{{ house.title }}</h4>
                  <p class="house-desc">{{ house.roomtype }} | {{ house.niandai }} | {{ house.floorlevel }}</p>
                  <div class="house-price">
                    <span class="price">¥{{ house.zongjia }}万</span>
                    <span class="area">{{ house.areanum }}㎡</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 右侧：系统介绍 -->
        <aside class="right-sidebar">
          <div class="intro-box">
            <h3 class="intro-title">系统介绍</h3>
            <div class="intro-content">
              <img src="/systemintro_picture3.jpg" alt="系统介绍" class="intro-img" />
              <p class="intro-text">
                本二手房信息系统为您提供真实可靠的房源信息、实时房价走势、最新政策公告，
                助力您高效完成二手房交易。我们致力于打造透明、安全、便捷的房产服务平台，
                让买房卖房更简单。
              </p>
            </div>
          </div>
        </aside>
      </div>
    </main>

    <!-- 底部 -->
    <footer class="footer">
      <div class="footer-container">
        <p>© 2026 二手房信息系统 版权所有</p>
        <p>客服热线：400-123-4567 | 邮箱：service@example.com</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
// 导入你提供的拦截器封装
import { request } from '@/utils/request'

const router = useRouter()

// 加载状态
const loading = ref(false)
const houseLoading = ref(false)

// 轮播图（仅保留静态图片路径）
const carouselList = ref([
  { image: '/picture1.jpg' },
  { image: '/picture2.jpg' },
  { image: '/picture3.jpg' }
])

// 接口数据存储
const announcementList = ref([])
const houseList = ref([])

// 跳转新闻详情
const toNewsDetail = (id) => {
  router.push({ path: '/home/newsDetail', query: { id } })
}

// 获取最新公告（使用你的request封装）
const getAnnouncementList = async () => {
  loading.value = true
  try {
    // 调用后端新闻列表接口
    const res = await request.get('/news', {
      page: 1,
      page_size: 5,
      title: '',
      typename: ''
    })
    // 适配接口返回格式（分页数据取items，非分页直接取res）
    announcementList.value = res.items || res
  } catch (error) {
    console.error('获取公告失败：', error)
    announcementList.value = []
  } finally {
    loading.value = false
  }
}

// 获取房源/城市数据（使用你的request封装）
const getHouseList = async () => {
  houseLoading.value = true
  try {
    const params = { 
        page: 1, 
        page_size: 6
    }
    // 1. 正确传递参数（单层 params）
    const res = await request.get('/city', params)

    houseList.value = res.items || []

  } catch (error) {
    console.error('获取数据失败：', error)
    // 错误时打印完整信息，方便排查
    if (error.response) {
      console.error('后端返回错误：', error.response.data)
      console.error('错误状态码：', error.response.status)
    }
    houseList.value = []
  } finally {
    houseLoading.value = false
  }
}

// 初始化加载
onMounted(() => {
  getAnnouncementList()
  getHouseList()
})
</script>

<style scoped>
.main-home {
  width: 100%;
}

/* 轮播图 */
.carousel-section {
  width: 100%;
  overflow: hidden;
}
.carousel-img {
  width: 100%;
  height: 500px;
  object-fit: cover;
}

/* 主体容器 */
.main-container {
  max-width: 1400px;
  margin: 30px auto;
  padding: 0 20px;
}
.content-wrapper {
  display: flex;
  gap: 30px;
}
.left-content {
  flex: 1;
  min-width: 0;
}

/* 公告模块 */
.announcement-box {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  margin-bottom: 30px;
}
.box-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 10px;
  border-bottom: 2px solid #409eff;
}
.box-title h3 {
  font-size: 18px;
  color: #333;
  margin: 0;
}
.more-link {
  font-size: 14px;
  color: #409eff;
  text-decoration: none;
}
.loading, .empty {
  text-align: center;
  padding: 20px;
  color: #999;
  font-size: 14px;
}
.announcement-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.announcement-item {
  display: flex;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
}
.announcement-item:hover {
  background: #f8f9fa;
}
.badge.new {
  background: #f56c6c;
  color: #fff;
  font-size: 12px;
  padding: 2px 6px;
  border-radius: 4px;
  margin-right: 10px;
}
.title {
  flex: 1;
  font-size: 14px;
  color: #333;
}
.date {
  font-size: 12px;
  color: #999;
  margin-left: 10px;
}

/* 房源模块 */
.house-list-box {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
}
.house-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-top: 20px;
}
.house-card {
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  transition: transform 0.3s;
}
.house-card:hover {
  transform: translateY(-4px);
}
.house-img {
  position: relative;
  height: 180px;
  overflow: hidden;
}
.house-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.tag {
  position: absolute;
  top: 10px;
  left: 10px;
  background: #409eff;
  color: #fff;
  font-size: 12px;
  padding: 4px 8px;
  border-radius: 4px;
}
.house-info {
  padding: 15px;
}
.house-title {
  font-size: 16px;
  color: #333;
  margin: 0 0 8px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.house-desc {
  font-size: 13px;
  color: #999;
  margin: 0 0 12px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.house-price {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.price {
  font-size: 18px;
  font-weight: 600;
  color: #f56c6c;
}
.area {
  font-size: 14px;
  color: #666;
}

/* 右侧系统介绍 */
.right-sidebar {
  width: 320px;
}
.intro-box {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
}
.intro-title {
  font-size: 18px;
  color: #333;
  margin: 0 0 16px 0;
  padding-bottom: 10px;
  border-bottom: 2px solid #409eff;
}
.intro-img {
  width: 100%;
  height: 180px;
  object-fit: cover;
  border-radius: 4px;
  margin-bottom: 15px;
}
.intro-text {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
}

/* 底部 */
.footer {
  background: #333;
  color: #fff;
  padding: 40px 20px;
  margin-top: 50px;
}
.footer-container {
  max-width: 1400px;
  margin: 0 auto;
  text-align: center;
  line-height: 1.8;
}
</style>