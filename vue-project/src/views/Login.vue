<template>
  <div class="login-container">
    <el-card class="login-card">
      <h2>登录</h2>
      <el-form :model="form" ref="formRef" label-width="0px">
        <el-form-item>
          <el-input v-model="form.account" placeholder="账号" />
        </el-form-item>
        <el-form-item>
          <el-input v-model="form.password" placeholder="密码" show-password />
        </el-form-item>
        <el-form-item>
          <el-select v-model="form.role" placeholder="角色">
            <el-option label="用户" value="user"></el-option>
            <el-option label="管理员" value="admin"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit">登录</el-button>
          <el-button type="text" @click="onRegister">注册</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRouter } from 'vue-router'
import { login } from '@/api/auth.js'

const router = useRouter()
const formRef = ref(null)
const form = ref({ account: '', password: '', role: 'user' })

const onSubmit = async () => {
  try {
    const payload = { account: form.value.account, password: form.value.password, role: form.value.role }
    const res = await login(payload)
    console.log('login res', res)
    if (res && res.code === 200 && res.data && res.data.token) {
      localStorage.setItem('token', res.data.token)
      ElMessage.success('登录成功')
      if (res.data.role === 'admin') {
        router.push('/admin/home')
      } else {
        router.push('/user/home')
      }
      return
    }
    showError('登录失败，请重试')
  } catch (err) {
    console.error('登录失败', err)
    const detail = err?.response?.data?.detail
    if (detail) {
      showError(detail)
    } else {
      showError('登录失败，请检查网络或稍后重试')
    }
  }
}

const onRegister = () => {
  router.push('/register')
}

function showError(message) {
  try {
    ElMessageBox.alert(message, '错误')
  } catch (e) {
    // 如果 Element Plus 的 MessageBox 不可用，则回退到 alert
    try { window.alert(message) } catch (_) { console.error(message) }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: calc(100vh - 80px);
}
.login-card {
  width: 360px;
  padding: 24px;
}
</style>
