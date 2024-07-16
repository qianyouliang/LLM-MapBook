import Vue from 'vue';
import VueRouter from 'vue-router';
import HomeView from "@/views/home-page/index.vue"


Vue.use(VueRouter);

const router = new VueRouter({
    mode: 'history',
    routes: [
      {
        path: '/',
        name: 'Home',
        component: HomeView
      },
    ]
  });

  export default router;
