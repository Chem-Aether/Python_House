<template>
  <div class="dashboard-container">
    <!-- 顶部标题栏 -->
    <div class="header">
      <div class="time">{{ currentTime }}</div>
      <h1>欢迎使用 二手房信息系统</h1>
    </div>

    <div class="grid-layout">
      <!-- 左上：年代占比（环形图） -->
      <div class="card">
        <div class="card-title">年代占比</div>
        <div ref="yearChartRef" class="chart"></div>
      </div>

      <!-- 中上：核心数据 + 轮播 -->
      <div class="card card-center">
        <div class="carousel">
          <div class="carousel-item">
            <img src="https://picsum.photos/200/150" alt="轮播图" />
            <div class="arrow left">&lt;</div>
            <div class="arrow right">&gt;</div>
          </div>
          <div class="quote">
            更加可爱。人在生命的严肃时刻，在悲伤与丧亲的阴影下，才最接近真实的自我。<br />
            在生活和事业的各个方面，才智的功能远不如性格，头脑的功能远不如心性，天分远不如自制力、毅力与教养。我始终认为
          </div>
        </div>
        <div class="stats-row">
          <div class="stat-item">
            <div class="stat-label">用户总数</div>
            <div class="stat-value">9</div>
          </div>
          <div class="stat-item">
            <div class="stat-label">二手房价总数</div>
            <div class="stat-value">350</div>
          </div>
        </div>
      </div>

      <!-- 右上：单价统计（柱状图） -->
      <div class="card">
        <div class="card-title">单价统计</div>
        <div ref="priceChartRef" class="chart"></div>
      </div>

      <!-- 左下：面积统计（面积图） -->
      <div class="card">
        <div class="card-title">面积统计</div>
        <div ref="areaChartRef" class="chart"></div>
      </div>

      <!-- 中下：TOP10 表格 -->
      <div class="card card-table">
        <div class="card-title">二手房价(单价TOP10)</div>
        <div class="table-wrapper">
          <table class="data-table">
            <thead>
              <tr>
                <th>标题</th>
                <th>图片</th>
                <th>面积</th>
                <th>单价</th>
                <th>房型</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, idx) in top10Data" :key="idx">
                <td>{{ item.title }}</td>
                <td><img :src="item.pic" alt="房源图" class="table-img" /></td>
                <td>{{ item.area }}</td>
                <td>{{ item.price }}</td>
                <td>{{ item.type }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 右下：房型占比（饼图） -->
      <div class="card">
        <div class="card-title">房型占比</div>
        <div ref="roomChartRef" class="chart"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'

// 响应式引用
const yearChartRef = ref(null)
const priceChartRef = ref(null)
const areaChartRef = ref(null)
const roomChartRef = ref(null)

let yearChart = null
let priceChart = null
let areaChart = null
let roomChart = null

// 当前时间
const currentTime = ref('2026年3月12日 星期四 23:05:57')

// TOP10 数据
const top10Data = ref([
  {
    title: '公园旁 外滩玺园 144平精装 全屋品牌纯实木 满二可按揭',
    pic: 'https://picsum.photos/80/60',
    area: 143.8,
    price: 10084,
    type: '3房2厅2厕'
  },
  // 可补充更多数据
])

// 年代占比图表配置
const initYearChart = () => {
  yearChart = echarts.init(yearChartRef.value)
  const option = {
    tooltip: { trigger: 'item' },
    legend: {
      orient: 'vertical',
      left: 'left',
      top: 20,
      textStyle: { color: '#fff' },
      data: ['2016年', '2010年', '2012年', '2020年', '2018年', '2019年', '2021年', '2015年']
    },
    series: [
      {
        name: '年代',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: { borderRadius: 10, borderColor: '#0a1a3a', borderWidth: 2 },
        label: { show: true, formatter: '{b}\n{d}%', color: '#fff' },
        emphasis: { label: { show: true, fontSize: 16, fontWeight: 'bold' } },
        data: [
          { value: 12, name: '2016年' },
          { value: 15, name: '2010年' },
          { value: 18, name: '2012年' },
          { value: 30, name: '2020年' },
          { value: 25, name: '2018年' },
          { value: 20, name: '2019年' },
          { value: 8, name: '2021年' },
          { value: 10, name: '2015年' }
        ]
      }
    ],
    backgroundColor: 'transparent'
  }
  yearChart.setOption(option)
}

// 单价统计柱状图
const initPriceChart = () => {
  priceChart = echarts.init(priceChartRef.value)
  const option = {
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      data: ['步梯二楼', '精装三室', '14个', '房本满二', '其他'],
      axisLabel: { color: '#fff', fontSize: 10 },
      axisLine: { lineStyle: { color: '#444' } }
    },
    yAxis: {
      type: 'value',
      axisLabel: { color: '#fff' },
      axisLine: { lineStyle: { color: '#444' } },
      splitLine: { lineStyle: { color: '#333' } }
    },
    series: [
      {
        name: '单价',
        type: 'bar',
        barWidth: '40%',
        itemStyle: {
          color: function (params) {
            const colors = ['#3398db', '#33b5db', '#33d5db', '#88d8a0', '#ffb347', '#ff80ab', '#33cc66']
            return colors[params.dataIndex]
          }
        },
        data: [8000, 6000, 5000, 4500, 6500, 1000, 9000, 12000]
      }
    ],
    backgroundColor: 'transparent'
  }
  priceChart.setOption(option)
}

// 面积统计面积图
const initAreaChart = () => {
  areaChart = echarts.init(areaChartRef.value)
  const option = {
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: ['A区', 'B区', 'C区', 'D区', 'E区', 'F区', 'G区', 'H区', 'I区'],
      axisLabel: { color: '#fff', fontSize: 10 },
      axisLine: { lineStyle: { color: '#444' } }
    },
    yAxis: {
      type: 'value',
      axisLabel: { color: '#fff' },
      axisLine: { lineStyle: { color: '#444' } },
      splitLine: { lineStyle: { color: '#333' } }
    },
    series: [
      {
        name: '面积',
        type: 'line',
        smooth: true,
        areaStyle: { color: 'rgba(51, 152, 219, 0.3)' },
        lineStyle: { color: '#3398db', width: 2 },
        itemStyle: { color: '#fff', borderColor: '#3398db', borderWidth: 2 },
        data: [1200, 800, 650, 600, 550, 300, 450, 100, 600]
      }
    ],
    backgroundColor: 'transparent'
  }
  areaChart.setOption(option)
}

// 房型占比饼图
const initRoomChart = () => {
  roomChart = echarts.init(roomChartRef.value)
  const option = {
    tooltip: { trigger: 'item', formatter: '{b}\n{d}%' },
    legend: {
      orient: 'vertical',
      right: 10,
      top: 20,
      textStyle: { color: '#fff', fontSize: 10 },
      data: ['3房2厅2厕', '3房2厅1厕', '2房2厅2厕', '4房2厅2厕', '3房1厅1厕', '3房1厅2厕', '6房3厅4厕', '6房3厅2厕']
    },
    series: [
      {
        name: '房型',
        type: 'pie',
        radius: '60%',
        center: ['40%', '50%'],
        itemStyle: { borderRadius: 5, borderColor: '#0a1a3a', borderWidth: 2 },
        label: { show: true, formatter: '{b}\n{d}%', color: '#fff', fontSize: 10 },
        emphasis: { label: { show: true, fontSize: 12, fontWeight: 'bold' } },
        data: [
          { value: 52.48, name: '3房2厅2厕' },
          { value: 36.74, name: '3房2厅1厕' },
          { value: 3.5, name: '2房2厅2厕' },
          { value: 3.79, name: '4房2厅2厕' },
          { value: 0.87, name: '3房1厅1厕' },
          { value: 0.87, name: '3房1厅2厕' },
          { value: 0.58, name: '6房3厅4厕' },
          { value: 1.17, name: '6房3厅2厕' }
        ]
      }
    ],
    backgroundColor: 'transparent'
  }
  roomChart.setOption(option)
}

// 窗口 resize 时重绘图表
const resizeCharts = () => {
  yearChart?.resize()
  priceChart?.resize()
  areaChart?.resize()
  roomChart?.resize()
}

onMounted(() => {
  initYearChart()
  initPriceChart()
  initAreaChart()
  initRoomChart()
  window.addEventListener('resize', resizeCharts)
})

onUnmounted(() => {
  yearChart?.dispose()
  priceChart?.dispose()
  areaChart?.dispose()
  roomChart?.dispose()
  window.removeEventListener('resize', resizeCharts)
})
</script>

<style scoped>
.dashboard-container {
  background-color: #0a1a3a;
  min-height: 100vh;
  padding: 16px;
  color: #fff;
  font-family: "Microsoft Yahei", sans-serif;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 24px;
  background: linear-gradient(90deg, #0f2a5a, #1a4a9a);
  border-radius: 8px;
  margin-bottom: 16px;
}

.header h1 {
  font-size: 24px;
  margin: 0;
}

.time {
  font-size: 14px;
  opacity: 0.8;
}

.grid-layout {
  display: grid;
  grid-template-columns: 1fr 1.5fr 1fr;
  grid-template-rows: auto auto;
  gap: 16px;
}

.card {
  background-color: #0f2a5a;
  border-radius: 8px;
  padding: 12px;
  position: relative;
  overflow: hidden;
}

.card-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 12px;
  padding-left: 8px;
  border-left: 4px solid #3398db;
}

.chart {
  width: 100%;
  height: 280px;
}

.card-center {
  grid-row: 1 / 2;
  grid-column: 2 / 3;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.carousel {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
}

.carousel-item {
  position: relative;
  width: 200px;
  height: 150px;
}

.carousel-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 8px;
}

.arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 24px;
  height: 24px;
  background: rgba(0, 0, 0, 0.5);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  cursor: pointer;
}

.arrow.left {
  left: 8px;
}

.arrow.right {
  right: 8px;
}

.quote {
  flex: 1;
  font-size: 14px;
  line-height: 1.6;
  color: #ddd;
}

.stats-row {
  display: flex;
  justify-content: center;
  gap: 40px;
}

.stat-item {
  text-align: center;
}

.stat-label {
  font-size: 14px;
  color: #aaa;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 20px;
  font-weight: bold;
  color: #fff;
}

.card-table {
  grid-row: 2 / 3;
  grid-column: 2 / 3;
}

.table-wrapper {
  max-height: 300px;
  overflow-y: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  color: #fff;
}

.data-table th,
.data-table td {
  border: 1px solid #2a4a7a;
  padding: 8px;
  text-align: center;
  font-size: 13px;
}

.data-table th {
  background-color: #1a4a9a;
}

.table-img {
  width: 60px;
  height: 40px;
  object-fit: cover;
  border-radius: 4px;
}
</style>