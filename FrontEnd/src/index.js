import Vue from "vue";
import App from "./App.vue";
import vuetify from "./plugins/vuetify.js";
import { router } from "./routes/index.js";
import "./style/reset.scss";

Vue.config.productionTip = false;

new Vue({
  render: (h) => h(App),
  router,
  vuetify,
}).$mount("#app");
