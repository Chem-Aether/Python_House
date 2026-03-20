<template>
  <div class="city-container">
    <!-- 搜索+新建区域：新增搜索按钮（修复标签闭合问题） -->
    <div class="header-bar">
      <div class="search-group">
        <el-input 
          v-model="q" 
          placeholder="按标题搜索" 
          clearable 
          @clear="handleSearch"
          @keyup.enter="handleSearch"
        ></el-input> <!-- 关键修复：补全闭合标签 -->
        <el-button type="primary" class="search-btn" @click="handleSearch">搜索</el-button>
      </div>
      <el-button type="primary" @click="openDialog()">新建</el-button>
    </div>

    <!-- 房源列表 -->
    <el-table 
      :data="items" 
      border 
      style="width:100%"
      v-loading="loading"
    >
      <el-table-column prop="id" label="ID" width="80"></el-table-column>
      <el-table-column prop="title" label="标题" min-width="200" show-overflow-tooltip></el-table-column>
      <el-table-column prop="address" label="地址" min-width="200" show-overflow-tooltip></el-table-column>
      <el-table-column prop="avgprice" label="单价" width="120"></el-table-column>
      <el-table-column prop="areanum" label="面积" width="120"></el-table-column>
      <el-table-column prop="roomtype" label="户型" width="120"></el-table-column>
      <el-table-column label="操作" width="220">
        <template #default="{row}">
          <el-button size="small" @click="openDialog(row)">编辑</el-button>
          <el-button size="small" type="danger" @click="remove(row.id)">删除</el-button>
        </template>
      </el-table-column>
      <template #empty>
        <div style="padding: 30px; text-align: center;">暂无房源数据</div>
      </template>
    </el-table>

    <!-- 分页 -->
    <div class="pagination-bar">
      <el-pagination 
        v-model:current-page="page" 
        :page-size="pageSize" 
        :total="total" 
        @current-change="fetchList"
        layout="prev, pager, next, jumper, ->, total"
      ></el-pagination>
    </div>

    <!-- 编辑/新建对话框 -->
    <el-dialog 
      v-model="dialogVisible" 
      :title="dialogTitle" 
      :width="dialogWidth"
      center
    >
      <el-form :model="form" label-width="80px" ref="formRef">
        <el-form-item label="标题" prop="title" :rules="[{required:true, message:'请输入标题'}]">
          <el-input v-model="form.title" placeholder="请输入房源标题"></el-input>
        </el-form-item>
        <el-form-item label="地址" prop="address" :rules="[{required:true, message:'请输入地址'}]">
          <el-input v-model="form.address" placeholder="请输入房源地址"></el-input>
        </el-form-item>
        <el-form-item label="单价" prop="avgprice" :rules="[{required:true, message:'请输入单价'}]">
          <el-input-number v-model="form.avgprice" :min="0" placeholder="请输入单价"></el-input-number>
        </el-form-item>
        <el-form-item label="面积" prop="areanum" :rules="[{required:true, message:'请输入面积'}]">
          <el-input-number v-model="form.areanum" :min="0" placeholder="请输入面积"></el-input-number>
        </el-form-item>
        <el-form-item label="户型" prop="roomtype" :rules="[{required:true, message:'请输入户型'}]">
          <el-input v-model="form.roomtype" placeholder="如：3室2厅"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="save">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { request } from '@/utils/request.js'

// 列表状态
const items = ref([])
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)
const q = ref('')
const loading = ref(false)
const dialogWidth = ref('80%')

// 对话框状态
const dialogVisible = ref(false)
const dialogTitle = ref('')
const formRef = ref(null)
const form = reactive({
  id: null,
  title: '',
  address: '',
  avgprice: null,
  areanum: null,
  roomtype: ''
})

// 屏幕适配
const handleResize = () => {
  dialogWidth.value = window.innerWidth < 768 ? '90%' : '60%'
}

// 获取列表数据
const fetchList = async () => {
  loading.value = true
  try {
    // 1. 修复请求参数传递方式（改为 params）
    const res = await request.get('/city', {
        page: page.value,
        page_size: pageSize.value,
        q: q.value
      })

    if (res && typeof res === 'object' && Array.isArray(res.items)) {
      items.value = res.items // 直接取 items 数组
      total.value = res.total // 直接使用接口返回的 total
    } else {
        items.value = []
        total.value = 0
    }
  } catch (err) {
    console.error('获取列表失败:', err)
    ElMessage.error('获取房源列表失败')
    items.value = []
    total.value = 0
  } finally {
    loading.value = false
  }
}
// 搜索方法
const handleSearch = () => {
  page.value = 1 // 搜索时重置页码到第一页
  fetchList()
}

// 打开对话框
const openDialog = (row = null) => {
  if (row) {
    dialogTitle.value = '编辑房源'
    Object.assign(form, JSON.parse(JSON.stringify(row)))
  } else {
    dialogTitle.value = '新建房源'
    Object.assign(form, { id: null, title: '', address: '', avgprice: null, areanum: null, roomtype: '' })
    formRef.value?.resetFields()
  }
  dialogVisible.value = true
}

// 保存数据
const save = async () => {
  try {
    await formRef.value.validate()
  } catch (err) {
    ElMessage.warning('请完善表单必填项')
    return
  }

  try {
    if (form.id) {
      await request.put(`/city/${form.id}`, form)
      ElMessage.success('更新成功')
    } else {
      await request.post('/city', form)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    fetchList()
  } catch (err) {
    console.error('保存失败:', err)
    ElMessage.error('保存失败：' + (err.message || '服务器异常'))
  }
}

// 删除数据
const remove = async (id) => {
  try {
    await ElMessageBox.confirm('确认删除该房源？', '删除确认', { type: 'warning' })
    await request.delete(`/city/${id}`)
    ElMessage.success('删除成功')
    fetchList()
  } catch (err) {
    if (err !== 'cancel') ElMessage.error('删除失败')
  }
}

// 生命周期
onMounted(() => {
  fetchList()
  handleResize()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.city-container {
  width: 100%;
  padding: 16px;
  box-sizing: border-box;
}

.header-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  gap: 12px;
}

/* 搜索组样式 */
.search-group {
  display: flex;
  align-items: center;
  width: 300px;
}

.search-group .el-input {
  flex: 1;
}

/* 搜索按钮样式 */
.search-btn {
  margin-left: 8px;
  white-space: nowrap;
}

.pagination-bar {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}

/* 响应式适配 */
@media (max-width: 768px) {
  .header-bar {
    flex-direction: column;
    align-items: stretch;
  }
  .search-group {
    width: 100%;
  }
}
</style>