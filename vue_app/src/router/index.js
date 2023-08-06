import { createRouter, createWebHashHistory } from "vue-router";

export default createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      path: "/",
      component: () => import("@/views/porn91.vue"),
    },
    {
      path: "/haijiao",
      component: () => import("@/views/haijiao.vue"),
    },
    {
      path: "/birdpaper",
      component: () => import("@/views/birdpaper.vue"),
    },
    {
      path: "/database",
      component: () => import("@/views/database.vue"),
    },
    {
      path: "/script",
      component: () => import("@/views/script.vue"),
    },
    {
      path: "/v2ray",
      component: () => import("@/views/v2ray.vue"),
    },
    {
      path: "/loader",
      component: () => import("@/views/loader.vue"),
    },
    {
      path: "/threejs",
      component: () => import("@/views/threejs/index.vue")
    },
  ],
});