<template>
  <div class="news-system">
    <!-- 标签页切换：新闻管理/分类管理 -->
    <el-tabs v-model="activeTab" type="card" class="tab-container">
      <!-- 新闻管理标签页 -->
      <el-tab-pane label="新闻管理" name="news">
        <div class="news-management">
          <!-- 新闻搜索栏 -->
          <div class="search-bar">
            <div class="search-group">
              <el-input
                v-model="searchForm.title"
                placeholder="请输入新闻标题"
                class="search-input"
                @keyup.enter="fetchNewsList"
              />
              <el-select
                v-model="searchForm.typename"
                placeholder="请选择分类"
                class="search-select"
                @change="fetchNewsList"
              >
                <el-option label="全部" value="" />
                <el-option
                  v-for="item in newsTypeList"
                  :key="item.id"
                  :label="item.typename"
                  :value="item.typename"
                />
              </el-select>
            </div>
            <div class="action-group">
              <el-button type="primary" :icon="Plus" @click="openNewsDialog()">添加新闻</el-button>
              <el-button
                type="danger"
                @click="handleBatchDeleteNews"
                :disabled="selectedNews.length === 0"
              >
                批量删除
              </el-button>
            </div>
          </div>

          <!-- 新闻列表 -->
          <el-table
            :data="newsList"
            v-loading="newsLoading"
            @selection-change="handleNewsSelectionChange"
            style="width: 100%"
            :header-cell-style="{ backgroundColor: '#409eff', color: '#fff' }"
            empty-text="暂无新闻数据，请添加"
          >
            <el-table-column type="selection" width="55" align="center" />
            <el-table-column label="序号" type="index" width="60" align="center" />
            <el-table-column prop="title" label="新闻标题" min-width="200" align="center" />
            <el-table-column prop="typename" label="分类名称" width="120" align="center" />
            <el-table-column prop="name" label="发布人" width="100" align="center" />
            <el-table-column prop="addtime" label="添加时间" width="200" align="center">
              <template #default="{ row }">
                {{ row.addtime ? new Date(row.addtime).toLocaleString() : '-' }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="200" align="center">
              <template #default="{ row }">
                <el-button size="small" type="primary" link @click="openNewsDialog(row, 'view')">
                  查看
                </el-button>
                <el-button size="small" type="primary" link @click="openNewsDialog(row, 'edit')">
                  修改
                </el-button>
                <el-button size="small" type="danger" link @click="handleDeleteNews(row.id)">
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>

          <!-- 新闻分页 -->
          <div class="pagination-bar" v-if="newsTotal > 0">
            <el-pagination
              v-model:current-page="newsPage"
              v-model:page-size="newsPageSize"
              :total="newsTotal"
              :page-sizes="[10, 20, 50, 100]"
              layout="total, sizes, prev, pager, next, jumper"
              @size-change="fetchNewsList"
              @current-change="fetchNewsList"
            />
          </div>
        </div>
      </el-tab-pane>

      <!-- 分类管理标签页 -->
      <el-tab-pane label="分类管理" name="type">
        <div class="type-management">
          <!-- 分类操作栏 -->
          <div class="type-action-bar">
            <el-input
              v-model="typeForm.typename"
              placeholder="请输入分类名称"
              class="type-input"
              @keyup.enter="handleAddType"
            />
            <el-button type="primary" :icon="Plus" @click="handleAddType">添加分类</el-button>
          </div>

          <!-- 分类列表 -->
          <el-table
            :data="newsTypeList"
            v-loading="typeLoading"
            style="margin-top: 16px"
            :header-cell-style="{ backgroundColor: '#409eff', color: '#fff' }"
            empty-text="暂无分类数据，请添加"
          >
            <el-table-column label="序号" type="index" width="60" align="center" />
            <el-table-column prop="typename" label="分类名称" min-width="200" align="center" />
            <el-table-column prop="addtime" label="创建时间" width="200" align="center">
              <template #default="{ row }">
                {{ row.addtime ? new Date(row.addtime).toLocaleString() : '-' }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="180" align="center">
              <template #default="{ row }">
                <el-button size="small" type="primary" link @click="openTypeDialog(row)">
                  修改
                </el-button>
                <el-button size="small" type="danger" link @click="handleDeleteType(row.id)">
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>

          <!-- 分类分页 -->
          <div class="pagination-bar" v-if="typeTotal > typePageSize">
            <el-pagination
              v-model:current-page="typePage"
              v-model:page-size="typePageSize"
              :total="typeTotal"
              :page-sizes="[10, 20, 50, 100]"
              layout="total, sizes, prev, pager, next, jumper"
              @size-change="fetchNewsTypeList"
              @current-change="fetchNewsTypeList"
            />
          </div>
        </div>
      </el-tab-pane>
    </el-tabs>

    <!-- 新闻新增/编辑/查看对话框 -->
    <el-dialog
      v-model="newsDialogVisible"
      :title="newsDialogTitle"
      width="800px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="newsFormRef"
        :model="newsForm"
        :rules="newsFormRules"
        label-width="80px"
        style="max-height: 600px; overflow-y: auto; padding-right: 10px"
      >
        <el-form-item label="新闻标题" prop="title">
          <el-input v-model="newsForm.title" placeholder="请输入新闻标题" maxlength="200" show-word-limit />
        </el-form-item>
        <el-form-item label="分类名称" prop="typename">
          <el-select v-model="newsForm.typename" placeholder="请选择分类">
            <el-option
              v-for="item in newsTypeList"
              :key="item.id"
              :label="item.typename"
              :value="item.typename"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="发布人" prop="name">
          <el-input v-model="newsForm.name" placeholder="请输入发布人名称" maxlength="50" show-word-limit />
        </el-form-item>
        <el-form-item label="简介">
          <el-input
            v-model="newsForm.introduction"
            type="textarea"
            placeholder="请输入新闻简介"
            rows="3"
            maxlength="500"
            show-word-limit
          />
        </el-form-item>
        <el-form-item label="封面图片">
          <el-upload
            class="avatar-uploader"
            action="/api/upload"
            :show-file-list="false"
            :on-success="handlePictureSuccess"
            :before-upload="(file) => {
              const isImage = file.type.startsWith('image/');
              if (!isImage) {
                ElMessage.error('只能上传图片格式！');
              }
              const isLt2M = file.size / 1024 / 1024 < 2;
              if (!isLt2M) {
                ElMessage.error('图片大小不能超过2MB！');
              }
              return isImage && isLt2M;
            }"
          >
            <img v-if="newsForm.picture" :src="newsForm.picture" class="avatar" />
            <div v-else class="avatar-uploader-icon"><el-icon><Plus /></el-icon></div>
          </el-upload>
        </el-form-item>
        <el-form-item label="新闻内容" prop="content">
          <el-input
            v-model="newsForm.content"
            type="textarea"
            placeholder="请输入新闻内容（支持Markdown）"
            rows="10"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="newsDialogVisible = false">取消</el-button>
        <el-button
          type="primary"
          @click="handleSaveNews"
          v-if="newsDialogType !== 'view'"
        >
          保存
        </el-button>
      </template>
    </el-dialog>

    <!-- 分类修改对话框 -->
    <el-dialog
      title="修改分类名称"
      v-model="typeDialogVisible"
      width="400px"
      :close-on-click-modal="false"
      :before-close="handleTypeDialogClose"
    >
      <el-form
        ref="typeFormRef"
        :model="editTypeForm"
        :rules="typeFormRules"
        label-width="80px"
      >
        <el-form-item label="分类名称" prop="typename">
          <el-input
            v-model="editTypeForm.typename"
            placeholder="请输入新分类名称"
            maxlength="200"
            show-word-limit
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <div style="text-align: center">
          <el-button @click="typeDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSaveType" :loading="typeSaving">保存</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch, nextTick } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
// 导入封装的 request 方法
import { request } from '@/utils/request.js'

// ====================== 基础变量 ======================
// 标签页控制
const activeTab = ref('news')

// ====================== 新闻管理相关 ======================
// 新闻搜索表单
const searchForm = reactive({
  title: '',
  typename: ''
})

// 新闻列表数据
const newsList = ref([])
const newsLoading = ref(false)
const newsPage = ref(1)
const newsPageSize = ref(10)
const newsTotal = ref(0)
const selectedNews = ref([])

// 新闻对话框
const newsDialogVisible = ref(false)
const newsDialogTitle = ref('')
const newsDialogType = ref('') // 'add' | 'edit' | 'view'
const newsFormRef = ref()
const newsForm = reactive({
  id: null,
  title: '',
  typename: '',
  name: '',
  introduction: '',
  picture: '',
  content: ''
})

// 新闻表单验证规则
const newsFormRules = {
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  typename: [{ required: true, message: '请选择分类', trigger: 'change' }],
  name: [{ required: true, message: '请输入发布人', trigger: 'blur' }],
  content: [{ required: true, message: '请输入内容', trigger: 'blur' }]
}

/**
 * 获取新闻列表
 */
const fetchNewsList = async () => {
  newsLoading.value = true
  try {
    const params = {
      skip: (newsPage.value - 1) * newsPageSize.value,
      limit: newsPageSize.value
    }

    if (searchForm.title.trim()) params.title = searchForm.title.trim()
    if (searchForm.typename.trim()) params.typename = searchForm.typename.trim()

    // 关键：路径末尾加 /
    const res = await request.get('/news/', params)

    console.log('新闻数据：', res)
    // 正确赋值
    newsList.value = res.items || []
    newsTotal.value = res.total || 0

  } catch (err) {
    console.error('获取新闻失败：', err)
    newsList.value = []
    newsTotal.value = 0
    ElMessage.error('获取新闻列表失败，请重试')
  } finally {
    newsLoading.value = false
  }
}

/**
 * 新闻表格多选
 */
const handleNewsSelectionChange = (selection) => {
  selectedNews.value = selection
}

/**
 * 打开新闻对话框
 */
const openNewsDialog = (row = null, type = 'add') => {
  newsDialogType.value = type
  if (row) {
    newsDialogTitle.value = type === 'view' ? '查看新闻' : '修改新闻'
    Object.assign(newsForm, JSON.parse(JSON.stringify(row)))
  } else {
    newsDialogTitle.value = '创建新闻'
    // 重置表单
    Object.assign(newsForm, {
      id: null,
      title: '',
      typename: '',
      name: '',
      introduction: '',
      picture: '',
      content: ''
    })
    nextTick(() => {
      newsFormRef.value?.clearValidate()
    })
  }
  newsDialogVisible.value = true
}

/**
 * 新闻图片上传成功
 */
const handlePictureSuccess = (res) => {
  newsForm.picture = res.data?.url || res.url || res
  if (!newsForm.picture) {
    ElMessage.warning('图片地址解析失败，请检查上传接口')
  }
}

/**
 * 保存新闻
 */
const handleSaveNews = async () => {
  try {
    await newsFormRef.value.validate()

    const submitData = { ...newsForm }
    // 移除空值
    Object.keys(submitData).forEach(key => {
      if (submitData[key] === '' || submitData[key] === null) {
        delete submitData[key]
      }
    })

    // 关键：路径末尾加 /
    if (newsForm.id) {
      await request.put(`/news/${newsForm.id}/`, submitData)
      ElMessage.success('新闻修改成功')
    } else {
      await request.post('/news/', submitData)
      ElMessage.success('新闻创建成功')
    }
    newsDialogVisible.value = false
    await fetchNewsList()
  } catch (err) {
    console.error('保存新闻失败:', err)
    ElMessage.error(`保存新闻失败：${err.message || '接口异常'}`)
  }
}

/**
 * 删除单个新闻
 */
const handleDeleteNews = async (id) => {
  try {
    await ElMessageBox.confirm('确认删除该新闻？', '删除确认', { type: 'warning' })
    // 关键：路径末尾加 /
    await request.delete(`/news/${id}/`)
    ElMessage.success('新闻删除成功')
    await fetchNewsList()
  } catch (err) {
    if (err !== 'cancel') {
      ElMessage.error(`删除新闻失败：${err.message || '接口异常'}`)
    }
  }
}

/**
 * 批量删除新闻
 */
const handleBatchDeleteNews = async () => {
  if (selectedNews.value.length === 0) {
    ElMessage.warning('请选择要删除的新闻')
    return
  }

  try {
    await ElMessageBox.confirm(`确认删除选中的 ${selectedNews.value.length} 条新闻？`, '批量删除', { type: 'warning' })

    // 循环删除
    for (const news of selectedNews.value) {
      await request.delete(`/news/${news.id}/`)
    }

    ElMessage.success('批量删除成功')
    await fetchNewsList()
  } catch (err) {
    if (err !== 'cancel') {
      ElMessage.error(`批量删除失败：${err.message || '接口异常'}`)
    }
  }
}

// ====================== 分类管理相关 ======================
const newsTypeList = ref([])
const typeLoading = ref(false)
const typeSaving = ref(false)

// 分类分页参数
const typePage = ref(1)
const typePageSize = ref(20)
const typeTotal = ref(0)

// 新增分类表单
const typeForm = reactive({
  typename: ''
})

// 修改分类表单
const editTypeForm = reactive({
  id: null,
  typename: ''
})

// 分类对话框
const typeDialogVisible = ref(false)
const typeFormRef = ref()

// 分类表单验证规则
const typeFormRules = {
  typename: [
    { required: true, message: '请输入分类名称', trigger: 'blur' },
    { min: 1, max: 200, message: '长度在 1 到 200 个字符', trigger: 'blur' }
  ]
}

/**
 * 获取分类列表
 */
const fetchNewsTypeList = async () => {
  typeLoading.value = true
  try {
    const params = {
      page: typePage.value,
      page_size: typePageSize.value
    }

    console.log('分类请求参数:', params)
    // 关键：路径末尾加 /
    const res = await request.get('/news/types/', params)

    console.log('分类响应数据:', res)
    // 正确赋值
    if (res && res.items) {
      newsTypeList.value = res.items
      typeTotal.value = res.total || 0
    } else if (Array.isArray(res)) {
      newsTypeList.value = res
      typeTotal.value = res.length
    } else {
      newsTypeList.value = []
      typeTotal.value = 0
    }

    if (newsTypeList.value.length === 0) {
      ElMessage.info('暂无新闻分类，请添加')
    }

  } catch (err) {
    console.error('获取分类失败详情:', err)
    newsTypeList.value = []
    typeTotal.value = 0

    if (err.response && err.response.status === 422) {
      ElMessage.error('分类接口路径错误，请检查后端路由配置')
    } else {
      ElMessage.error(`获取分类列表失败：${err.message || '接口请求异常'}`)
    }
  } finally {
    typeLoading.value = false
  }
}

/**
 * 添加分类
 */
const handleAddType = async () => {
  const typename = typeForm.typename.trim()
  if (!typename) {
    ElMessage.warning('请输入分类名称')
    return
  }

  try {
    // 关键：路径末尾加 /
    await request.post('/news/types/', { typename })

    ElMessage.success('分类添加成功')
    typeForm.typename = ''
    typePage.value = 1
    await fetchNewsTypeList()
    await fetchNewsList()

  } catch (err) {
    console.error('添加分类失败:', err)
    ElMessage.error(`添加分类失败：${err.message || '分类名称可能已存在'}`)
  }
}

/**
 * 打开分类修改对话框
 */
const openTypeDialog = (row) => {
  editTypeForm.id = row.id
  editTypeForm.typename = row.typename
  typeDialogVisible.value = true
  nextTick(() => {
    typeFormRef.value?.clearValidate()
  })
}

/**
 * 保存分类修改
 */
const handleSaveType = async () => {
  try {
    await typeFormRef.value.validate()

    const typename = editTypeForm.typename.trim()
    if (!typename) {
      ElMessage.warning('分类名称不能为空')
      return
    }

    typeSaving.value = true

    // 关键：路径末尾加 /
    await request.put(`/news/types/${editTypeForm.id}/`, { typename })

    ElMessage.success('分类修改成功')
    typeDialogVisible.value = false
    await fetchNewsTypeList()
    await fetchNewsList()

  } catch (err) {
    console.error('修改分类失败:', err)
    ElMessage.error(`修改分类失败：${err.message || '分类名称可能已存在'}`)
  } finally {
    typeSaving.value = false
  }
}

/**
 * 删除分类
 */
const handleDeleteType = async (id) => {
  try {
    await ElMessageBox.confirm(
      '确认删除该分类？\n注意：删除后关联新闻的分类不会自动修改',
      '删除确认',
      {
        type: 'warning',
        confirmButtonText: '确认删除',
        cancelButtonText: '取消'
      }
    )

    // 关键：路径末尾加 /
    await request.delete(`/news/types/${id}/`)

    ElMessage.success('分类删除成功')
    await fetchNewsTypeList()
    await fetchNewsList()

  } catch (err) {
    if (err !== 'cancel') {
      console.error('删除分类失败:', err)
      ElMessage.error(`删除分类失败：${err.message || '删除失败，可能分类正在被使用'}`)
    }
  }
}

/**
 * 关闭分类对话框
 */
const handleTypeDialogClose = () => {
  typeFormRef.value?.clearValidate()
  typeDialogVisible.value = false
}

// ====================== 监听与初始化 ======================
// 监听标签页切换
watch(activeTab, (newVal) => {
  if (newVal === 'type') {
    fetchNewsTypeList()
  }
})

// 初始化加载
onMounted(async () => {
  await fetchNewsTypeList()
  await fetchNewsList()
})
</script>

<style scoped>
.news-system {
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  min-height: calc(100vh - 120px);
}

.tab-container {
  margin-bottom: 16px;
}

/* 新闻管理样式 */
.news-management {
  padding: 10px 0;
}

.search-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.search-group {
  display: flex;
  align-items: center;
  gap: 12px;
}

.search-input {
  width: 240px;
}

.search-select {
  width: 180px;
}

.action-group {
  display: flex;
  gap: 12px;
}

/* 分类管理样式 */
.type-management {
  padding: 10px 0;
}

.type-action-bar {
  display: flex;
  align-items: center;
  gap: 12px;
}

.type-input {
  width: 240px;
}

/* 通用样式 */
.pagination-bar {
  margin-top: 20px;
  text-align: center;
}

.avatar-uploader {
  :deep(.el-upload) {
    border: 1px dashed #409eff;
    border-radius: 6px;
    cursor: pointer;
    width: 100px;
    height: 100px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s;
  }
  :deep(.el-upload:hover) {
    border-color: #66b1ff;
  }
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #409eff;
}

.avatar {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 6px;
}

:deep(.el-table th) {
  background-color: #409eff !important;
  color: #fff !important;
}

:deep(.el-table td) {
  text-align: center;
}

:deep(.el-button--small) {
  height: 28px;
  padding: 0 12px;
  font-size: 12px;
}
</style>