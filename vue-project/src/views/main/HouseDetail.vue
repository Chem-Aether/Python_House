<template>
  <div class="house-detail-page">
    <!-- 返回 -->
    <div class="back-btn">
      <el-button type="text" @click="router.back()">← 返回</el-button>
    </div>

    <div class="detail-container">
      <!-- 左侧图片 -->
      <div class="left-img-section">
        <el-carousel height="400px" :interval="4000" ref="carouselRef">
          <el-carousel-item v-for="(img, idx) in houseImages" :key="idx">
            <img :src="img" alt="" class="detail-img" />
          </el-carousel-item>
        </el-carousel>

        <div class="thumb-list">
          <div
            v-for="(img, idx) in houseImages"
            :key="idx"
            class="thumb-item"
            @click="carouselRef?.setActiveItem(idx)"
          >
            <img :src="img" alt="" />
          </div>
        </div>
      </div>

      <!-- 右侧信息 -->
      <div class="right-info-section">
        <div class="title-bar">
          <h1 class="house-title">{{ houseData.title }}</h1>
          <el-button type="warning" size="small">
            <el-icon><Star /></el-icon>
            收藏({{ houseData.collect_count || 0 }})
          </el-button>
        </div>

        <div class="info-table">
          <div class="info-row">
            <div class="info-item">
              <span class="label">类型</span>
              <span class="value">{{ houseData.usetype || '普通住宅' }}</span>
            </div>
            <div class="info-item">
              <span class="label">年代</span>
              <span class="value">{{ houseData.niandai || '未知' }}</span>
            </div>
          </div>
          <div class="info-row">
            <div class="info-item">
              <span class="label">面积</span>
              <span class="value">{{ houseData.areanum }}㎡</span>
            </div>
            <div class="info-item">
              <span class="label">单价</span>
              <span class="value">{{ houseData.avgprice || 0 }}元/㎡</span>
            </div>
          </div>
          <div class="info-row">
            <div class="info-item">
              <span class="label">总价</span>
              <span class="value price">¥{{ houseData.zongjia }}万</span>
            </div>
            <div class="info-item">
              <span class="label">楼层</span>
              <span class="value">{{ houseData.floorlevel || '未知' }}</span>
            </div>
          </div>
          <div class="info-row">
            <div class="info-item">
              <span class="label">房型</span>
              <span class="value">{{ houseData.roomtype || '未知' }}</span>
            </div>
            <div class="info-item">
              <span class="label">来源</span>
              <a :href="houseData.laiyuan" target="_blank" class="link">查看原链接</a>
            </div>
          </div>
          <div class="info-row">
            <div class="info-item">
              <span class="label">地址</span>
              <span class="value">{{ houseData.address || '未知' }}</span>
            </div>
            <div class="info-item">
              <span class="label">点击</span>
              <span class="value">{{ houseData.click_count || 0 }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ====================== 极简评论区 ====================== -->
    <div class="simple-comment">
      <div class="comment-head">
        <h3>全部评论（{{ commentList.length }}）</h3>
      </div>

      <!-- 发表评论 -->
      <div class="comment-publish">
        <el-input
          v-model="commentContent"
          type="textarea"
          :rows="3"
          placeholder="写下你的评论..."
          class="input"
        />
        <div class="text-right mt-10">
          <el-button type="primary" @click="submitComment" :disabled="!commentContent.trim()">
            发表评论
          </el-button>
        </div>
      </div>

      <!-- 评论列表 -->
      <div class="comment-list">
        <div v-for="item in commentList" :key="item.id" class="comment-item">
          <div class="avatar">
            <img :src="item.avatar" alt="" />
          </div>
          <div class="content">
            <div class="name">{{ item.user_name }}</div>
            <div class="text">{{ item.content }}</div>
            <div class="meta">
              <span>{{ item.create_time }}</span>
              <span class="like" @click="likeComment(item.id)">
                <el-icon><svg t="1774002416447" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="1669" width="200" height="200"><path d="M832 364.8h-147.2s19.2-64 32-179.2c6.4-57.6-38.4-115.2-102.4-121.6h-12.8c-51.2 0-83.2 32-102.4 76.8l-38.4 96c-32 64-57.6 102.4-76.8 115.2-25.6 12.8-121.6 12.8-128 12.8H128c-38.4 0-64 25.6-64 57.6v480c0 32 25.6 57.6 64 57.6h646.4c96 0 121.6-64 134.4-153.6l51.2-307.2c6.4-70.4-6.4-134.4-128-134.4z m-576 537.6H128V422.4h128v480z m640-409.6l-51.2 307.2c-12.8 57.6-12.8 102.4-76.8 102.4H320V422.4c44.8 0 70.4-6.4 89.6-19.2 32-12.8 64-64 108.8-147.2 25.6-64 38.4-96 44.8-102.4 6.4-19.2 19.2-32 44.8-32h6.4c32 0 44.8 32 44.8 51.2-12.8 102.4-32 166.4-32 166.4l-25.6 83.2h243.2c19.2 0 32 0 44.8 12.8 12.8 12.8 6.4 38.4 6.4 57.6z" p-id="1670"></path></svg></el-icon>
                {{ item.like_count }}
              </span>
            </div>
          </div>
        </div>

        <div v-if="commentList.length === 0" class="empty">暂无评论</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { request } from '@/utils/request'
import { ElMessage } from 'element-plus'
import { Star,  } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const carouselRef = ref()
const houseId = route.query.id

const houseData = ref({})
const houseImages = ref([])
const commentContent = ref('')

// 极简评论数据
const commentList = ref([
  {
    id: 1,
    user_name: '用户001',
    avatar: 'https://picsum.photos/48/48?random=1',
    content: '房源信息真实有效，位置不错。',
    create_time: '2026-03-20 12:30',
    like_count: 5
  },
  {
    id: 2,
    user_name: '用户002',
    avatar: 'https://picsum.photos/48/48?random=2',
    content: '价格合理，交通方便，值得推荐。',
    create_time: '2026-03-20 15:20',
    like_count: 2
  }
])

// 获取详情
const getHouseDetail = async () => {
  if (!houseId) {
    ElMessage.error('无效ID')
    router.back()
    return
  }
  try {
    const res = await request.get(`/city/${houseId}`)
    houseData.value = res || {}
    houseImages.value = [res.picture || 'https://picsum.photos/800/400']
  } catch (e) {
    console.error(e)
    ElMessage.error('加载失败')
  }
}

// 发表评论
const submitComment = () => {
  if (!commentContent.value.trim()) return ElMessage.warning('请输入内容')
  commentList.value.unshift({
    id: Date.now(),
    user_name: '我',
    avatar: 'https://picsum.photos/48/48?random=99',
    content: commentContent.value,
    create_time: new Date().toLocaleString(),
    like_count: 0
  })
  commentContent.value = ''
  ElMessage.success('发表成功')
}

// 点赞
const likeComment = (id) => {
  const item = commentList.value.find(i => i.id === id)
  if (item) item.like_count++
}

onMounted(() => {
  getHouseDetail()
})
</script>

<style scoped>
.house-detail-page {
  max-width: 1200px;
  margin: 20px auto;
  padding: 0 20px;
}
.back-btn {
  margin-bottom: 20px;
}
.detail-container {
  display: flex;
  gap: 30px;
  margin-bottom: 40px;
}
.left-img-section {
  flex: 1;
}
.detail-img {
  width: 100%;
  height: 400px;
  object-fit: cover;
  border-radius: 8px;
}
.thumb-list {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}
.thumb-item {
  width: 80px;
  height: 60px;
  overflow: hidden;
  border-radius: 4px;
  cursor: pointer;
}
.thumb-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.right-info-section {
  flex: 1;
}
.title-bar {
  background: #f56c6c;
  color: #fff;
  padding: 14px 20px;
  border-radius: 8px 8px 0 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.house-title {
  font-size: 20px;
  margin: 0;
}
.info-table {
  border: 1px solid #eee;
  border-top: none;
  padding: 20px;
  border-radius: 0 0 8px 8px;
}
.info-row {
  display: flex;
  margin-bottom: 16px;
}
.info-item {
  flex: 1;
  display: flex;
}
.label {
  width: 60px;
  color: #666;
}
.value {
  color: #333;
}
.price {
  color: #f56c6c;
  font-size: 18px;
  font-weight: bold;
}
.link {
  color: #409eff;
}

/* ====================== 极简评论区样式 ====================== */
.simple-comment {
  margin-top: 40px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}
.comment-head h3 {
  font-size: 18px;
  margin: 0 0 20px 0;
  font-weight: 500;
}
.comment-publish {
  margin-bottom: 30px;
}
.comment-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.comment-item {
  display: flex;
  gap: 12px;
  padding-bottom: 16px;
  border-bottom: 1px dashed #eee;
}
.avatar img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}
.content {
  flex: 1;
}
.name {
  font-weight: 500;
  margin-bottom: 4px;
}
.text {
  line-height: 1.6;
  margin-bottom: 6px;
  color: #333;
}
.meta {
  font-size: 12px;
  color: #999;
  display: flex;
  gap: 16px;
}
.like {
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
}
.like:hover {
  color: #409eff;
}
.empty {
  color: #999;
  text-align: center;
  padding: 40px 0;
}
.text-right {
  text-align: right;
}
.mt-10 {
  margin-top: 10px;
}
</style>