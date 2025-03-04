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

