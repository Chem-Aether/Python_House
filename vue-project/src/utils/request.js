// src/utils/requests.js
import axios from 'axios';
import { ElMessage } from 'element-plus'; // 如果您使用Element Plus

// 创建axios实例
const instance = axios.create({
  baseURL: 'http://localhost:8000/',
  timeout: 10000, // 增加超时时间

});

// 请求拦截器
instance.interceptors.request.use(
  (config) => {
    // 在发送请求之前做些什么
    // 从 localStorage 获取 token 并注入到请求头
    try {
      const token = localStorage.getItem('token')
      if (token) {
        config.headers = config.headers || {}
        config.headers.Authorization = `Bearer ${token}`
      }
    } catch (err) {
      console.warn('注入 token 失败', err)
    }

    return config;
  },
  (error) => {
    // 对请求错误做些什么
    console.error('请求错误:', error);
    return Promise.reject(error);
  }
);

// 响应拦截器
instance.interceptors.response.use(
  (response) => {
    // 2xx 范围内的状态码都会触发该函数
    // 对响应数据做点什么
    console.log('收到响应:', response.status, response.data);
        if (Array.isArray(response.data)) {
      return response.data;
    }
    
    // 根据您的API结构调整
    if (response.data && response.data.code === 200) {
      return response.data;
    } else {
      return Promise.reject(response.data);
    }
  },
  (error) => {
    // 超出 2xx 范围的状态码都会触发该函数
    // 对响应错误做点什么
    console.error('响应错误:', error);
    
    if (error.response) {
      // 服务器返回了错误状态码
      const { status, data } = error.response;
      
      switch (status) {
        case 400:
          ElMessage.error(data.message || '请求参数错误');
          break;
        case 401:
          ElMessage.error('未授权，请重新登录');
          localStorage.removeItem('token');
          sessionStorage.removeItem('token');
          // 跳转到登录页
          window.location.href = '/login';
          break;
        case 403:
          ElMessage.error('拒绝访问');
          break;
        case 404:
          ElMessage.error('请求资源不存在');
          break;
        case 500:
          ElMessage.error(data.message || '服务器内部错误');
          break;
        case 502:
          ElMessage.error('网关错误');
          break;
        case 503:
          ElMessage.error('服务不可用');
          break;
        case 504:
          ElMessage.error('网关超时');
          break;
        default:
          ElMessage.error(`连接错误${status}`);
      }
    } else if (error.request) {
      // 请求已经成功发起，但没有收到响应
      ElMessage.error('网络异常，请检查网络连接');
    } else {
      // 发送请求时出了点问题
      ElMessage.error('请求失败，请稍后重试');
    }
    
    return Promise.reject(error);
  }
);

// 封装通用请求方法
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
  },
  patch(url, data = {}, config = {}) {
    return instance.patch(url, data, config);
  }
};

// 默认导出实例
export default instance;