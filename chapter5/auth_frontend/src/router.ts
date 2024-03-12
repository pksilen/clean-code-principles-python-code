import { createRouter, createWebHistory } from "vue-router";
import AuthorizationCallback from "@/views/AuthCallbackView.vue";
import AuthorizationError from "@/views/AuthErrorView.vue";
import HomeView from "@/views/HomeView.vue";
import LoginView from "@/views/LoginView.vue";

const routes = [
  {
    path: "/",
    name: "login",
    component: LoginView,
  },
  {
    path: "/auth",
    name: "auth",
    component: AuthorizationCallback,
  },
  {
    path: "/auth-error",
    name: "auth-error",
    component: AuthorizationError,
  },
  {
    path: "/home",
    name: "home",
    component: HomeView,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
