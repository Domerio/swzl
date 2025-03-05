import Vue from 'vue';
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import App from './App.vue';
import axios from 'axios'
import router from "@/router";

Vue.use(ElementUI);
// 正确挂载到Vue原型
Vue.prototype.$axios = axios

new Vue({
  router,
  render: h => h(App),
}).$mount('#app');

// 配置 axios
Vue.prototype.$axios = axios.create({
  baseURL: process.env.VUE_APP_API_URL || 'http://localhost:8000'
})

// 使用 axios 的请求拦截器，在发送请求之前进行一些处理
axios.interceptors.request.use(config => {
  // 添加请求头 token
  config.headers.Authorization = localStorage.getItem('token');
  return config;
});

// 使用 axios 的响应拦截器来处理响应数据或错误
axios.interceptors.response.use(
  // 当响应成功时，直接返回响应对象
  response => response,
  // 当响应失败时，处理错误
  error => {
    // 检查错误响应的状态码是否为 401（未授权）
    if (error.response.status === 401) {
      // Token 失效时返回登录页
      this.$router.push('/login');
    }
    return Promise.reject(error);
  }
);

