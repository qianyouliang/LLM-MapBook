import Vue from 'vue'
import App from './App.vue'
import router from '@/router/index.js'
// 引入VueRouter
import VueRouter from 'vue-router'
// 引入Element UI
import ElementUI from 'element-ui';
import axios from 'axios';
import '../public/css/dark/index.css';
// import 'element-ui/lib/theme-chalk/index.css';
import * as echarts from "echarts";
import VueBus from 'vue-bus';
import * as ol from 'ol';
import hljs from 'highlight.js';
import {marked} from 'marked';
import 'github-markdown-css';
import 'highlight.js/styles/atom-one-dark.css';
import store from "./store/index.js"

console.log(marked); // 应该输出一个函数或对象
Vue.use(VueBus);
Vue.use(ElementUI);
Vue.use(VueRouter);

// 全局注册echarts
Vue.prototype.$echarts = echarts;

// Vue 配置
Vue.config.productionTip = false;

// 全局绑定 axios
Vue.prototype.$axios = axios;

// 将 ol 对象添加到 Vue 的原型中
Vue.prototype.$ol = ol;
window.ol = ol;
window.$message = ElementUI.Message;
window.axios = axios;
// 配置 marked
marked.setOptions({
  renderer: new marked.Renderer(),
  // highlight: function(code, language) {
  //   const validLanguage = hljs.getLanguage(language) ? language : 'plaintext';
  //   return hljs.highlight(validLanguage, code).value;
  // },
  pedantic: false,
  gfm: true,
  breaks: false,
  sanitize: false,
  smartLists: true,
  smartypants: false,
  xhtml: false
});
window.marked = marked;

// 封装自定义全局指令
// Vue.directive('markdown', {
//   bind(el, binding) {
//     console.log('Markdown directive bind:', binding.value);
//     el.innerHTML = marked(binding.value);
//     el.querySelectorAll('pre code').forEach(block => {
//       hljs.highlightBlock(block);
//     });
//   },
//   update(el, binding) {
//     console.log('Markdown directive update:', binding.value);
//     el.innerHTML = marked(binding.value);
//     el.querySelectorAll('pre code').forEach(block => {
//       hljs.highlightBlock(block);
//     });
//   }
// });

new Vue({
  router,
  store,
  render: h => h(App),
}).$mount('#app')
