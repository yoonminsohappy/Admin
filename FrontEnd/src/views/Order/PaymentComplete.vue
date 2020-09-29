<template>
  <div class="page">
    <h3 class="page-title">
      주문 관리
      <small>결제완료 관리</small>
    </h3>
    <filter-area></filter-area>
  </div>
</template>

<script>
import FilterArea from "../../components/Filter/Filter";
export default {
  components: { FilterArea },
};
</script>

<style scoped lang="scss">
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
</style>
