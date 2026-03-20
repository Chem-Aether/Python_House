import axios from 'axios';
import { ElMessage, ElMessageBox } from 'element-plus';

// 创建axios实例
const instance = axios.create({
  baseURL: 'http://localhost:8000/',
  timeout: 10000,
  headers: { 'Content-Type': 'application/json;charset=utf-8' }
});

// 请求拦截器
instance.interceptors.request.use(
  (config) => {
    // Token注入
    const token = localStorage.getItem('token') || sessionStorage.getItem('token');
    if (token && token.trim()) {
      config.headers.Authorization = `Bearer ${token.trim()}`;
    }
    return config;
  },
  (error) => {
    console.error('请求初始化错误:', error);
    ElMessage.error('请求发送失败');
    return Promise.reject(error);
  }
);

// 响应拦截器（核心修改：精准判断 401 原因，避免误退出）
instance.interceptors.response.use(
  (response) => {
    console.log('后端原始响应:', response.data);
    return response.data;
  },
  (error) => {
    // 取消请求不提示错误
    if (axios.isCancel(error)) {
      console.warn('请求已取消:', error.message);
      return Promise.reject({ isCancel: true, message: error.message });
    }

    // 网络错误/无响应（不触发退出）
    if (!error.response) {
      ElMessage.error(error.message.includes('timeout') ? '请求超时，请重试' : '网络异常，请检查后端服务');
      return Promise.reject(error);
    }

    // HTTP状态码错误处理
    const { status, data } = error.response;
    const errorMsg = data?.msg || data?.message || data?.detail || '操作失败';

    // ===================== 核心修改：精准判断 401 场景 =====================
    if (status === 401) {
      // 只在后端明确返回「Token 无效/过期」时才触发退出
      const needLogout = [
        '无效 token', 
        'Token 已过期', 
        '登录状态已过期', 
        '未授权',
        '账号或密码错误' // 登录接口的 401 不触发（但登录接口一般不会走这里）
      ].some(keyword => errorMsg.includes(keyword));

      if (needLogout) {
        ElMessageBox.confirm(
          '登录状态已过期，请重新登录',
          '权限验证失败',
          {
            confirmButtonText: '去登录',
            cancelButtonText: '取消',
            type: 'warning'
          }
        ).then(() => {
          localStorage.removeItem('token');
          sessionStorage.removeItem('token');
          window.location.href = `/login?redirect=${encodeURIComponent(window.location.href)}`;
        });
      } else {
        // 其他 401 场景（如 Token 格式错、路由错）只提示，不退出
        ElMessage.error(`权限验证失败：${errorMsg}`);
      }
    } 
    // 其他状态码处理（保持不变，不触发退出）
    else if (status === 403) {
      ElMessage.error(`权限拒绝：${errorMsg}`);
    } else if (status === 404) {
      ElMessage.error(`资源不存在：${errorMsg}`);
    } else if (status === 500) {
      ElMessage.error(`服务器错误：${errorMsg}`);
    } else {
      ElMessage.error(`请求失败 [${status}]：${errorMsg}`);
    }
    
    return Promise.reject(error);
  }
);

// 封装请求方法
export const request = {
  get(url, params = {}, config = {}) {
    return instance.get(url, { params, ...config });
  },
  post(url, data = {}, config = {}) {
    return instance.post(url, data, config);
  },
  put(url, data = {}, config = {}) {
    return instance.put(url, data, config);
  },
  delete(url, config = {}) {
    return instance.delete(url, config);
  }
};

export default instance;