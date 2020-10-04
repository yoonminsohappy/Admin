<template>
  <div>
    <page-bar></page-bar>
    <product-btn></product-btn>
    <scroll-table></scroll-table>
  </div>
</template>

<script>
import PageBar from "./Components/PageBar";
import ProductBtn from "./Components/ProductExcel";
import ScrollTable from "./Components/ScrollTable";

export default {
  components: {
    PageBar,
    ProductBtn,
    ScrollTable,
  },
};
</script>

<style>
</style>