<template>
  <div class="secondhand-page">
    <!-- 顶部筛选搜索栏 -->
    <div class="filter-header">
      <div class="container">
        <el-row :gutter="20" align="middle">
          <!-- 房源标题搜索 -->
          <el-col :span="8">
            <el-input
              v-model="searchForm.q"
              placeholder="请输入房源标题/地址搜索"
              clearable
              @keyup.enter="handleSearch"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
              <template #suffix>
                <el-button type="primary" @click="handleSearch">搜索</el-button>
              </template>
            </el-input>
          </el-col>

          <!-- 户型筛选 -->
          <el-col :span="6">
            <el-select
              v-model="searchForm.roomtype"
              placeholder="户型筛选"
              clearable
              @change="fetchHouseList"
            >
              <el-option label="全部户型" value=""></el-option>
              <el-option label="3房2厅1厕" value="3房2厅1厕"></el-option>
              <el-option label="2房1厅1厕" value="2房1厅1厕"></el-option>
              <el-option label="4房2厅2厕" value="4房2厅2厕"></el-option>
            </el-select>
          </el-col>

          <!-- 价格区间筛选 -->
          <el-col :span="6">
            <el-select
              v-model="searchForm.priceRange"
              placeholder="价格区间"
              clearable
              @change="fetchHouseList"
            >
              <el-option label="全部价格" value=""></el-option>
              <el-option label="50万以下" value="0-50"></el-option>
              <el-option label="50-100万" value="50-100"></el-option>
              <el-option label="100-200万" value="100-200"></el-option>
              <el-option label="200万以上" value="200+"></el-option>
            </el-select>
          </el-col>

          <!-- 重置筛选 -->
          <el-col :span="4">
            <el-button type="default" @click="resetSearch">重置筛选</el-button>
          </el-col>
        </el-row>
      </div>
    </div>

    <!-- 房源列表区域 -->
    <div class="container main-content">
      <!-- 加载状态 -->
      <div v-if="loading" class="loading-container">
        <el-skeleton :rows="8" animated></el-skeleton>
      </div>

      <!-- 无数据状态 -->
      <div v-else-if="houseList.length === 0" class="empty-container">
        <el-empty description="暂无符合条件的房源数据"></el-empty>
      </div>

      <!-- 房源列表（多列布局） -->
      <div v-else class="house-grid">
        <div 
          v-for="(house, index) in houseList" 
          :key="house.id" 
          class="house-card"
          @click="toHouseDetail(house.id)"
        >
          <div class="house-img">
            <img :src="house.picture" :alt="house.title">
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

      <!-- 分页控件 -->
      <div class="pagination-container" v-if="!loading && houseList.length > 0">
        <el-pagination
          v-model:current-page="page"
          v-model:page-size="pageSize"
          :total="total"
          :page-sizes="[12, 24, 36]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="fetchHouseList"
        ></el-pagination>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Search } from '@element-plus/icons-vue'
import { request } from '@/utils/request'
import { ElMessage } from 'element-plus'

const router = useRouter()

// 加载状态
const loading = ref(false)
// 分页参数（匹配 FastAPI 接口）
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)

// 搜索筛选表单
const searchForm = reactive({
  q: '',         // 对应接口 q 参数（标题/地址搜索）
  roomtype: '',  // 户型筛选
  priceRange: '' // 价格区间
})

// 房源列表数据
const houseList = ref([])

// 获取房源列表
const fetchHouseList = async () => {
  loading.value = true
  try {
    const params = {
      page: page.value,
      page_size: pageSize.value,
      q: searchForm.q.trim() || undefined,
      roomtype: searchForm.roomtype || undefined
    }

    const res = await request.get('/city', params)
    
    // 解析分页对象
    houseList.value = res.items || []  // 取列表数据
    total.value = res.total || 0       // 取总条数

    // 图片兜底
    houseList.value = houseList.value.map(item => ({
      ...item,
      picture: item.picture || '/default-house.jpg',
      usetype: item.usetype || '普通住宅'
    }))
  } catch (error) {
    console.error('获取房源列表失败：', error)
    ElMessage.error('获取房源数据失败，请稍后重试')
    houseList.value = []
    total.value = 0
  } finally {
    loading.value = false
  }
}

const handleSearch = async () => {
    page.value = 1,
    pageSize.value = 20,
    fetchHouseList()
}

// 分页大小改变
const handleSizeChange = (val) => {
  pageSize.value = val
  fetchHouseList()
}

// 重置筛选条件
const resetSearch = () => {
  searchForm.q = ''
  searchForm.roomtype = ''
  searchForm.priceRange = ''
  page.value = 1
  fetchHouseList()
}

// 跳转到房源详情页
const toHouseDetail = (houseId) => {
  router.push({
    path: '/home/houseDetail',
    query: { id: houseId }
  })
}

// 初始化加载
onMounted(() => {
  fetchHouseList()
})
</script>

<style scoped>
/* 页面整体样式 */
.secondhand-page {
  background-color: #f5f7fa;
  min-height: 100vh;
}

/* 筛选头部 */
.filter-header {
  background-color: #fff;
  padding: 16px 0;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* 主内容区 */
.main-content {
  padding: 20px 0;
}

.loading-container, .empty-container {
  padding: 40px 0;
  text-align: center;
}

/* 房源列表布局（完全匹配你的模板） */
.house-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-top: 20px;
}

/* 房源卡片样式（匹配你的模板） */
.house-card {
  background-color: #fff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  transition: transform 0.3s;
  cursor: pointer;
}

.house-card:hover {
  transform: translateY(-4px);
}

/* 房源图片 */
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

/* 房源信息 */
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

/* 分页控件 */
.pagination-container {
  margin-top: 30px;
  text-align: right;
}

/* 响应式适配 */
@media (max-width: 992px) {
  .house-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 576px) {
  .house-grid {
    grid-template-columns: 1fr;
  }
}
</style>