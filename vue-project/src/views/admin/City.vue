<template>
  <div>
    <div style="display:flex;justify-content:space-between;margin-bottom:12px">
      <el-input v-model="q" placeholder="按标题搜索" style="width:300px" clearable @clear="fetchList"/>
      <div>
        <el-button type="primary" @click="openDialog()">新建</el-button>
      </div>
    </div>

    <el-table :data="items" style="width:100%">
      <el-table-column prop="id" label="ID" width="80"/>
      <el-table-column prop="title" label="标题"/>
      <el-table-column prop="address" label="地址"/>
      <el-table-column prop="avgprice" label="单价" width="120"/>
      <el-table-column prop="areanum" label="面积" width="120"/>
      <el-table-column prop="roomtype" label="户型" width="120"/>
      <el-table-column label="操作" width="220">
        <template #default="{row}">
          <el-button size="small" @click="openDialog(row)">编辑</el-button>
          <el-button size="small" type="danger" @click="remove(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <div style="margin-top:12px;display:flex;justify-content:flex-end">
      <el-pagination :current-page.sync="page" :page-size="pageSize" :total="total" @current-change="fetchList" layout="prev, pager, next"/>
    </div>

    <el-dialog :title="dialogTitle" :visible.sync="dialogVisible">
      <el-form :model="form" label-width="80px">
        <el-form-item label="标题">
          <el-input v-model="form.title"/>
        </el-form-item>
        <el-form-item label="地址">
          <el-input v-model="form.address"/>
        </el-form-item>
        <el-form-item label="单价">
          <el-input v-model.number="form.avgprice"/>
        </el-form-item>
        <el-form-item label="面积">
          <el-input v-model.number="form.areanum"/>
        </el-form-item>
        <el-form-item label="户型">
          <el-input v-model="form.roomtype"/>
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
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { request } from '@/utils/request.js'

const items = ref([])
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)
const q = ref('')

const dialogVisible = ref(false)
const dialogTitle = ref('')
const form = reactive({ id: null, title: '', address: '', avgprice: null, areanum: null, roomtype: '' })

const fetchList = async () => {
  try {
    const res = await request.get('/city', { page: page.value, page_size: pageSize.value, q: q.value })
    if (res && Array.isArray(res)) {
      items.value = res
      // 简单处理 total：后端暂时不返回总数，前端根据返回条数估计
      total.value = res.length >= pageSize.value ? page.value * pageSize.value + 1 : (page.value - 1) * pageSize.value + res.length
    }
  } catch (err) {
    ElMessage.error('获取房源列表失败')
  }
}

const openDialog = (row = null) => {
  if (row) {
    dialogTitle.value = '编辑房源'
    Object.assign(form, row)
  } else {
    dialogTitle.value = '新建房源'
    Object.assign(form, { id: null, title: '', address: '', avgprice: null, areanum: null, roomtype: '' })
  }
  dialogVisible.value = true
}

const save = async () => {
  try {
    if (form.id) {
      await request.put(`/city/${form.id}`, { title: form.title, address: form.address, avgprice: form.avgprice, areanum: form.areanum, roomtype: form.roomtype })
      ElMessage.success('更新成功')
    } else {
      await request.post('/city', { title: form.title, address: form.address, avgprice: form.avgprice, areanum: form.areanum, roomtype: form.roomtype })
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    fetchList()
  } catch (err) {
    ElMessage.error('保存失败')
  }
}

const remove = async (id) => {
  try {
    await ElMessageBox.confirm('确认删除该条房源吗？', '删除确认', { type: 'warning' })
    await request.delete(`/city/${id}`)
    ElMessage.success('删除成功')
    fetchList()
  } catch (err) {
    // 取消会抛错，忽略
  }
}

onMounted(fetchList)
</script>

<style scoped>
.el-input { width: 100% }
</style>
