import Vue from "vue"; 
import App from "./App.vue";
import vuetify from "./plugins/vuetify.js";
import { router } from "./routes/index.js";
import { store } from "./store/store"
import "./style/reset.scss";
import './components/Fontawesome/fontAwesomeIcon'
Vue.config.productionTip = false;

new Vue({
  router,
  store,
  vuetify,
  render: (h) => h(App),
}).$mount("#app");
