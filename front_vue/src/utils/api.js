import axios from 'axios';

// 根据环境变量设置基础URL
// 在Docker环境中使用/api作为基础路径，由Nginx代理到后端
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

// 创建axios实例
const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
  timeout: 15000 // 超时设置为15秒
});

// 请求拦截器
api.interceptors.request.use(config => {
  // 可以在这里添加认证token等
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, error => {
  return Promise.reject(error);
});

// 响应拦截器
api.interceptors.response.use(
  response => response,
  error => {
    // 处理错误
    console.error('API错误:', error);
    
    // 统一处理特定错误
    if (error.response) {
      // 处理401未授权
      if (error.response.status === 401) {
        // 清除登录信息并重定向到登录页
        localStorage.removeItem('token');
        window.location.href = '/login';
      }
    }
    
    return Promise.reject(error);
  }
);

export default api;
