<template>
  <div id="app">
    <div class="window-container">
      <nav-bar v-if="noSideBar"></nav-bar>
      <SideBar v-if="noSideBar" />
      <router-view :class="on" />
    </div>
    <Footer />
  </div>
</template>

<script>
import SideBar from "./components/SideBar/SideBar";
import NavBar from "./components/Nav/Nav";
import Footer from "./components/Footer/Footer";

export default {
  components: { SideBar, Footer, NavBar },
  computed: {
    noSideBar() {
      if (
        this.$route.name.indexOf("Login") &&
        this.$route.name.indexOf("Signup")
      ) {
        return -1;
      }
    },
    on() {
      if (
        this.$route.name.indexOf("Login") &&
        this.$route.name.indexOf("Signup")
      ) {
        return "admin-frame";
      }
    },
  },
};
</script>

<style scoped>
.window-container {
  display: flex;
}
.admin-frame {
  width: 100%;
  padding: 25px 20px 20px 20px;
  margin-top: 45px;
}
@media (min-width: 1000px) and (max-width: 1500px) {
  .admin-frame {
    min-height: 699px;
  }
}
</style>
