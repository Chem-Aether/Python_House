import { request } from '@/utils/request.js'

export const login = (data) => {
  // 假设后端登录接口为 POST /auth/login
  return request.post('/auth/login', data)
}

export const logout = () => {
  localStorage.removeItem('token')
  return Promise.resolve()
}

export default { login }
