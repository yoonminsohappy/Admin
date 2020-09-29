<template>
  <div class="list_filter_area">
    <filter-search></filter-search>
    <filter-date></filter-date>
    <filter-md></filter-md>
  </div>
</template>

<script>
import FilterSearch from "./Components/FilterSearch";
import FilterDate from "./Components/FilterDate";
import FilterMd from "./Components/FilterMd";

export default {
  components: { FilterSearch, FilterDate, FilterMd },
};
</script>

<style scoped lang="scss">
.list_filter_area {
  border: 3px solid #eee;
  padding-left: 10px;
  margin-bottom: 20px;
}
</style>
