// frontend/src/main.js
import Vue from 'vue';
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import App from './App.vue';
import axios from 'axios'
import router from "@/router";
import store from "@/store";

Vue.use(ElementUI);
// 正确挂载到Vue原型
Vue.prototype.$axios = axios

new Vue({
    router,
    store, // 挂载到Vue原型
    render: h => h(App),
    scrollBehavior(to, from) {
        console.log('[路由轨迹]', from.path, '→', to.path)
    },
    created() {
    console.log('[Vue初始化] Store状态:', this.$store.state)
  }
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
// 全局错误处理
Vue.config.errorHandler = (err, vm, info) => {
  console.error('[全局异常]', err, info)
  vm.$message.error(`应用程序错误: ${err.message}`)
}


