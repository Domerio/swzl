// frontend/src/main.js
import Vue from 'vue';
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import App from './App.vue';
import router from './router';
import store from './store';
import axios from 'axios';
import dayjs from 'dayjs'

Vue.use(ElementUI);
Vue.config.productionTip = false;

Vue.prototype.$dayjs = dayjs
// 配置axios
const service = axios.create({
    baseURL: process.env.VUE_APP_API_URL || '/api',
    timeout: 5000
});

// 请求拦截器
service.interceptors.request.use(
    config => {
        const token = store.state.token;
        if (token) {
            config.headers['Authorization'] = `Token ${token}`;
        }
        return config;
    },
    error => {
        console.log(error);
        return Promise.reject(error);
    }
);

// 响应拦截器
// 为service对象的响应拦截器添加处理逻辑
service.interceptors.response.use(
    // 当响应成功时，直接返回响应数据
    response => response.data,
    // 当响应失败时，处理错误
    error => {
        // 如果错误对象中包含response属性，说明服务器有响应
        if (error.response) {
            // 根据响应状态码进行不同的处理
            switch (error.response.status) {
                case 401:
                    // 如果状态码为401，表示未授权，触发登出操作
                    store.dispatch('logout');
                    // 重定向到登录页面
                    router.push('/login');
                    // 显示错误消息：登录已过期，请重新登录
                    Vue.prototype.$message.error('登录已过期，请重新登录');
                    break;
                case 403:
                    // 如果状态码为403，表示禁止访问，显示错误消息：没有权限访问
                    Vue.prototype.$message.error('没有权限访问');
                    break;
                case 404:
                    // 如果状态码为404，表示资源不存在，显示错误消息：请求的资源不存在
                    Vue.prototype.$message.error('请求的资源不存在');
                    break;
                case 500:
                    // 如果状态码为500，表示服务器错误，显示错误消息：服务器错误
                    Vue.prototype.$message.error('服务器错误');
                    break;
                default:
                    // 对于其他状态码，显示服务器返回的错误消息或默认的未知错误消息
                    Vue.prototype.$message.error(error.response.data.message || '未知错误');
            }
        } else {
            // 如果错误对象中没有response属性，说明是网络错误，显示错误消息：网络错误，请检查您的网络连接
            Vue.prototype.$message.error('网络错误，请检查您的网络连接');
        }
        // 返回一个rejected的Promise，以便调用者可以捕获到错误
        return Promise.reject(error);
    }
);

Vue.prototype.$http = service;

new Vue({
    router,
    store,
    render: h => h(App)
}).$mount('#app');

// 全局错误处理
// 设置Vue的全局错误处理函数
Vue.config.errorHandler = (err, vm, info) => {
    // 在控制台输出错误信息，包括错误对象和错误信息
    console.error('[全局异常]', err, info);
    // 使用Vue实例的$message方法显示错误信息
    // 这里假设vm是Vue组件实例，$message是用于显示消息的插件或方法
    vm.$message.error(`应用程序错误: ${err.message}`);
}


