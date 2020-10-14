<template>
  <div id="app">
    <div class="window-container">
      <nav-bar v-if="noSideBar"></nav-bar>
      <SideBar v-if="noSideBar" />
      <div class="background-maker"><router-view :class="on" /></div>
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
        this.$route.name.indexOf("Signup") &&
        this.$route.name.indexOf("ProductRegist")
      ) {
        return "admin-frame";
      } else if (!this.$route.name.indexOf("ProductRegist")) {
        return "product-resgist";
      }
    },
  },
};
</script>

<style scoped>
.window-container {
  width: 100vw;
  display: flex;
}
.background-maker {
  background-color: #35363a;
  width: 100%;
  height: 100%;
}
.product-resgist,
.admein-fram {
  border-radius: 0 0 0 10px;
  background-color: white;
}
.admin-frame {
  min-height: 699px;
  background-color: white;
  padding: 25px 20px 20px 20px;
  margin-top: 45px;
}
</style>
