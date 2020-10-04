<template>
  <div class="position">
    <spiner v-if="fetchStatus"></spiner>
    <div class="page">
      <h3 class="page-title">
        주문 관리
        <small>결제완료 관리</small>
      </h3>
      <filter-area></filter-area>
      <product-list></product-list>
    </div>
  </div>
</template>

<script>
import FilterArea from "../../components/Filter/Filter";
import ProductList from "../../components/ProductList/ProductList";
import Spiner from "../../components/Spiner/Spiner";
import { mapGetters } from "vuex";
export default {
  computed: {
    ...mapGetters("order", ["isFetch"]),
    fetchStatus() {
      return this.isFetch;
    },
  },
  components: { FilterArea, ProductList, Spiner },
};
</script>

<style scoped lang="scss">
.position {
  position: relative;
  .page {
    background-color: #fafafa;
    .page-title {
      font-size: 26px;
      font-weight: 300;
      letter-spacing: -1px;
      color: #666;
      margin: 0px 0px 15px 0px;

      small {
        font-size: 14px;
        letter-spacing: 0px;
        font-weight: 300;
        color: #888;
      }
    }
  }
}
</style>
