// frontend/src/main.js
import Vue from 'vue';
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import App from './App.vue';
import router from './router';
import store from './store';
import axios from 'axios';

Vue.use(ElementUI);
Vue.config.productionTip = false;

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
service.interceptors.response.use(
    response => response.data,
    error => {
        if (error.response) {
            switch (error.response.status) {
                case 401:
                    store.dispatch('logout');
                    router.push('/login');
                    Vue.prototype.$message.error('登录已过期，请重新登录');
                    break;
                case 403:
                    Vue.prototype.$message.error('没有权限访问');
                    break;
                case 404:
                    Vue.prototype.$message.error('请求的资源不存在');
                    break;
                case 500:
                    Vue.prototype.$message.error('服务器错误');
                    break;
                default:
                    Vue.prototype.$message.error(error.response.data.message || '未知错误');
            }
        } else {
            Vue.prototype.$message.error('网络错误，请检查您的网络连接');
        }
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
Vue.config.errorHandler = (err, vm, info) => {
    console.error('[全局异常]', err, info);
    vm.$message.error(`应用程序错误: ${err.message}`);
}


