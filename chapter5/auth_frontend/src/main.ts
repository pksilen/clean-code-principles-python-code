import { setupFetch } from "@/tryMakeHttpRequest";
setupFetch();
import { createApp } from "vue";
import { createPinia } from "pinia";
import AppView from "@/views/AppView.vue";
import router from "@/router";

if ("serviceWorker" in navigator) {
  await navigator.serviceWorker.register("/serviceWorker.js");
}

const app = createApp(AppView);
const pinia = createPinia();
app.use(pinia);
app.use(router);
app.mount("#app");
