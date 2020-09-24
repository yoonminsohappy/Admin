<template>
  <div id="app">
    <div>
      <SideBar v-if="noSideBar" />
      <router-view :class="on" />
    </div>
    <Footer />
  </div>
</template>

<script>
import SideBar from "./components/SideBar/SideBar";
import Footer from "./components/Footer/Footer";

export default {
  components: { SideBar, Footer },
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
.admin-frame {
  margin: 45px 0 0 215px;
  min-height: 855px;
  padding: 25px 20px 20px 20px;
}
@media (min-width: 1000px) and (max-width: 1500px) {
  .admin-frame {
    min-height: 699px;
  }
}
</style>
