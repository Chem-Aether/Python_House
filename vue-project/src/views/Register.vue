<template>
  <div class="register-container">
    <el-card class="register-card">
      <h2>注册</h2>
      <el-form :model="form" ref="formRef" label-width="0px">
        <el-form-item>
          <el-input v-model="form.account" placeholder="账号" />
        </el-form-item>
        <el-form-item>
          <el-input v-model="form.password" placeholder="密码" show-password />
        </el-form-item>
          <el-form-item>
            <el-input v-model="form.xingming" placeholder="姓名" />
          </el-form-item>
  <!-- 角色选择已移除：只能注册普通用户 -->
        <el-form-item>
          <el-button type="primary" @click="onSubmit">注册</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import { request } from '@/utils/request.js'

const router = useRouter()
const formRef = ref(null)
const form = ref({ account: '', password: '', xingming: '' })

const onSubmit = async () => {
  try {
  const res = await request.post('/auth/register', { account: form.value.account, password: form.value.password, xingming: form.value.xingming })
    if (res && res.code === 200) {
      ElMessage.success('注册成功，请登录')
      router.push('/login')
      return
    }
    ElMessage.error('注册失败')
  } catch (err) {
    ElMessage.error(err?.response?.data?.detail || '注册失败')
  }
}
</script>

<style scoped>
.register-container { display:flex; justify-content:center; align-items:center; height: calc(100vh - 80px); }
.register-card { width: 360px; padding: 24px }
</style>
