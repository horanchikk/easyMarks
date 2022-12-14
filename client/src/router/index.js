import { createWebHashHistory, createRouter } from "vue-router";

import appPage from '../views/app/appPage.vue'
import homePage from '../views/homePage.vue'
import testPage from '../views/testPage.vue'


const routes = [
  {
    name: "app",
    path: "/app",
    component: appPage,
  },
  {
    name: "home",
    path: "/auth",
    component: homePage,
  },
  {
    name: "design",
    path: "/design",
    component: testPage,
  },
  {
    name: "redirect",
    path: "/",
    component: () => import('../views/redirect.vue')
  }
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
