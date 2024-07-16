import Vue from 'vue'
import App from './App.vue'
import router from '@/router/index.js'
//引入VueRouter
import VueRouter from 'vue-router'
// 引入element UI
import ElementUI from 'element-ui';
import axios from 'axios';
import 'element-ui/lib/theme-chalk/index.css';
import * as echarts from "echarts";
import VueBus from 'vue-bus';
import * as ol from 'ol';
Vue.use(VueBus);
Vue.use(ElementUI);
Vue.use(VueRouter);
Vue.prototype.$echarts = echarts;
Vue.config.productionTip = false
Vue.prototype.$message = ElementUI.Message;
// 全局绑定 axios
Vue.prototype.$axios = axios;
// 将 ol 对象添加到 Vue 的原型中
Vue.prototype.$ol = ol;
Window.ol = ol;
window.$message = ElementUI.Message;

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
 