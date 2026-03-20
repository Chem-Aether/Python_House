<template>
  <div class="user-management">
    <!-- 搜索栏 -->
    <div class="search-bar">
      <div class="search-group">
        <el-form :inline="true" :model="searchForm" class="search-form">
          <el-form-item label="用户账号">
            <el-input v-model="searchForm.zhanghao" placeholder="用户账号" clearable />
          </el-form-item>
          <el-form-item label="用户姓名">
            <el-input v-model="searchForm.xingming" placeholder="用户姓名" clearable />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" :icon="Search" @click="fetchUsers">查询</el-button>
          </el-form-item>
        </el-form>
      </div>
      <div class="action-group">
        <el-button type="primary" :icon="Plus" @click="openDialog()">添加</el-button>
        <el-button 
          type="danger" 
          :icon="Delete" 
          :disabled="!selectedUsers.length"
          @click="handleBatchDelete"
        >
          删除
        </el-button>
      </div>
    </div>

    <!-- 用户列表 -->
    <el-table 
      :data="userList" 
      v-loading="loading"
      @selection-change="handleSelectionChange"
      style="margin-top: 16px"
    >
      <el-table-column type="selection" width="50" />
      <el-table-column label="序号" type="index" width="60" />
      <el-table-column prop="zhanghao" label="用户账号" sortable />
      <el-table-column prop="xingming" label="用户姓名" sortable />
      <el-table-column prop="xingbie" label="性别" sortable width="80">
        <template #default="{ row }">
          <span>{{ row.xingbie || '未知' }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="shouji" label="手机" sortable />
      <el-table-column prop="touxiang" label="头像" width="120">
        <template #default="{ row }">
          <el-image 
            v-if="row.touxiang" 
            :src="row.touxiang" 
            :preview-src-list="[row.touxiang]"
            style="width: 80px; height: 80px; object-fit: cover"
          />
          <span v-else>无头像</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="280">
        <template #default="{ row }">
          <el-button-group>
            <el-button size="small" type="primary" :icon="View" @click="openDialog(row, 'view')">查看</el-button>
            <el-button size="small" type="success" :icon="Edit" @click="openDialog(row)">修改</el-button>
            <el-button size="small" type="danger" :icon="Delete" @click="handleDelete(row.id)">删除</el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <div class="pagination-bar" style="margin-top: 16px; text-align: right">
      <el-pagination
        v-model:current-page="page"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="fetchUsers"
        @current-change="fetchUsers"
      />
    </div>

    <!-- 新增/编辑/查看对话框 -->
    <el-dialog 
      :title="dialogTitle" 
      v-model="dialogVisible" 
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form 
        ref="formRef" 
        :model="form" 
        :rules="formRules" 
        label-width="100px"
        :disabled="dialogType === 'view'"
      >
        <el-form-item label="用户账号" prop="zhanghao">
          <el-input v-model="form.zhanghao" :disabled="form.id" placeholder="请输入账号" />
        </el-form-item>
        <el-form-item label="密码" prop="mima" v-if="dialogType !== 'view'">
          <el-input 
            v-model="form.mima" 
            type="password" 
            placeholder="新建必填，编辑留空则不修改" 
            show-password
          />
        </el-form-item>
        <el-form-item label="用户姓名" prop="xingming">
          <el-input v-model="form.xingming" placeholder="请输入姓名" />
        </el-form-item>
        <el-form-item label="性别" prop="xingbie">
          <el-select v-model="form.xingbie" placeholder="请选择性别">
            <el-option label="男" value="男" />
            <el-option label="女" value="女" />
          </el-select>
        </el-form-item>
        <el-form-item label="年龄" prop="nianling">
          <el-input-number v-model="form.nianling" :min="0" :max="150" placeholder="请输入年龄" />
        </el-form-item>
        <el-form-item label="手机" prop="shouji">
          <el-input v-model="form.shouji" placeholder="请输入手机号" />
        </el-form-item>
        <el-form-item label="头像" prop="touxiang" v-if="dialogType !== 'view'">
          <el-upload
            class="avatar-uploader"
            action="/api/upload"
            :show-file-list="false"
            :on-success="handleAvatarSuccess"
            accept="image/*"
          >
            <img v-if="form.touxiang" :src="form.touxiang" class="avatar" />
            <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
          </el-upload>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" v-if="dialogType !== 'view'" @click="handleSave">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, Plus, View, Edit, Delete } from '@element-plus/icons-vue'
import { request } from '@/utils/request.js'

// 搜索表单
const searchForm = reactive({
  zhanghao: '',
  xingming: ''
})

// 列表数据
const userList = ref([])
const loading = ref(false)
const page = ref(1)
const pageSize = ref(10)
const total = ref(0)
const selectedUsers = ref([])

// 对话框
const dialogVisible = ref(false)
const dialogTitle = ref('')
const dialogType = ref('') // 'add' | 'edit' | 'view'
const formRef = ref()
const form = reactive({
  id: null,
  zhanghao: '',
  mima: '',
  xingming: '',
  xingbie: '',
  nianling: null,
  shouji: '',
  touxiang: ''
})

// 表单验证规则
const formRules = {
  zhanghao: [
    { required: true, message: '请输入用户账号', trigger: 'blur' }
  ],
  xingming: [
    { required: true, message: '请输入用户姓名', trigger: 'blur' }
  ],
  mima: [
    { required: (rule, value) => !form.id, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ]
}

// 获取用户列表（核心修复：参数传递方式）
const fetchUsers = async () => {
  loading.value = true
  try {
    const skip = (page.value - 1) * pageSize.value
    // ✅ 参数名和后端完全匹配：skip/limit/zhanghao/xingming
    const res = await request.get('/users', {
      skip: skip,
      limit: pageSize.value,
      zhanghao: searchForm.zhanghao,  // 对应后端 zhanghao 参数
      xingming: searchForm.xingming   // 对应后端 xingming 参数
    })
    userList.value = res || []
    total.value = res.length // 若后端返回分页总数，可改为 res.total
  } catch (err) {
    console.error('获取用户列表失败:', err)
    ElMessage.error('获取用户列表失败')
  } finally {
    loading.value = false
  }
}

// 表格多选
const handleSelectionChange = (selection) => {
  selectedUsers.value = selection
}

// 打开对话框
const openDialog = (row = null, type = 'add') => {
  dialogType.value = type
  if (row) {
    dialogTitle.value = type === 'view' ? '查看用户' : '修改用户'
    Object.assign(form, JSON.parse(JSON.stringify(row)))
    form.mima = '' // 编辑时清空密码
  } else {
    dialogTitle.value = '添加用户'
    Object.assign(form, {
      id: null,
      zhanghao: '',
      mima: '',
      xingming: '',
      xingbie: '',
      nianling: null,
      shouji: '',
      touxiang: ''
    })
    formRef.value?.resetFields()
  }
  dialogVisible.value = true
}

// 头像上传成功
const handleAvatarSuccess = (res) => {
  form.touxiang = res.data.url // 根据上传接口返回格式调整
}

// 保存用户
const handleSave = async () => {
  try {
    await formRef.value.validate()
    const submitData = { ...form }
    // 编辑时如果密码为空，删除密码字段（避免覆盖）
    if (form.id && !submitData.mima) delete submitData.mima

    if (form.id) {
      // 修改用户
      await request.put(`/users/${form.id}`, submitData)
      ElMessage.success('修改成功')
    } else {
      // 新增用户
      await request.post('/users', submitData)
      ElMessage.success('添加成功')
    }
    dialogVisible.value = false
    fetchUsers() // 刷新列表
  } catch (err) {
    console.error('保存失败:', err)
    ElMessage.error('保存失败')
  }
}

// 删除单个用户
const handleDelete = async (id) => {
  try {
    await ElMessageBox.confirm('确认删除该用户？', '删除确认', { type: 'warning' })
    await request.delete(`/users/${id}`)
    ElMessage.success('删除成功')
    fetchUsers() // 刷新列表
  } catch (err) {
    if (err !== 'cancel') ElMessage.error('删除失败')
  }
}

// 批量删除
const handleBatchDelete = async () => {
  if (!selectedUsers.value.length) return
  try {
    await ElMessageBox.confirm(`确认删除选中的 ${selectedUsers.value.length} 个用户？`, '批量删除', { type: 'warning' })
    // 批量删除（可优化为后端批量接口）
    for (const user of selectedUsers.value) {
      await request.delete(`/users/${user.id}`)
    }
    ElMessage.success('批量删除成功')
    fetchUsers() // 刷新列表
  } catch (err) {
    if (err !== 'cancel') ElMessage.error('批量删除失败')
  }
}

// 初始化加载列表
onMounted(() => {
  fetchUsers()
})
</script>

<style scoped>
.user-management {
  padding: 20px;
  background: #fff;
  border-radius: 4px;
}

.search-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-group {
  display: flex;
  align-items: center;
}

.action-group {
  display: flex;
  gap: 8px;
}

.avatar-uploader {
  :deep(.el-upload) {
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
    cursor: pointer;
    width: 100px;
    height: 100px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
}

.avatar {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 6px;
}

/* 按钮样式优化 */
.el-button {
  /* 确保文字居中对齐 */
  display: inline-flex;
  align-items: center;
  justify-content: center;
  /* 统一按钮高度 */
  height: 32px;
  /* 统一内边距 */
  padding: 8px 15px;
  /* 确保文字不换行 */
  white-space: nowrap;
}

/* 表格内小按钮样式优化 */
.el-button--small {
  height: 28px;
  padding: 5px 12px;
  font-size: 12px;
}

/* 操作列按钮容器 */
.el-table__body .el-table__cell .el-button {
  /* 确保表格内按钮紧凑排列 */
  margin: 2px 4px 2px 0;
}

/* 主要按钮样式微调 */
.el-button--primary {
  /* 确保图标和文字垂直居中 */
  line-height: 1;
}

/* 图标按钮文字对齐 */
.el-button [class*="el-icon"] + span {
  margin-left: 4px;
}
</style>