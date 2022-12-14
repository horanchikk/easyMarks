import { createWebHashHistory, createRouter } from "vue-router";

const routes = [
  {
    name: "home",
    path: "/auth",
    component: () => import("../views/homePage.vue"),
  },
  {
    name: "design",
    path: "/design",
    component: () => import("../views/testPage.vue"),
  },
  {
    name: "app",
    path: "/app",
    component: () => import("../views/app/appPage.vue"),
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
