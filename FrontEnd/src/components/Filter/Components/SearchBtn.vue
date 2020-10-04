<template>
  <div class="filter-btn">
    <input type="button" value="검색" class="search-btn" @click="fetchFilter" />
    <input type="button" value="초기화" class="default-btn" />
  </div>
</template>

<script>
import { mapActions } from "vuex";

export default {
  methods: {
    ...mapActions("order", ["fetchFilter"]),
  },
};
</script>

<style scoped lang="scss">
.filter-btn {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 10px;
  font-size: 13px;
  font-weight: 400;

  input {
    border-radius: 0px;
    padding: 6px 50px;
    border: 1px solid transparent;
  }
  .search-btn {
    color: #fff;
    background-color: #428bca;
    border-color: #357ebd;
    outline: none !important;
    margin-right: 3px;
    &:hover {
      color: #fff;
      background-color: #3071a9;
      border-color: #285e8e;
    }
  }
  .default-btn {
    color: #333;
    background-color: #fff;
    border-color: #e5e5e5;
    outline: none !important;
    &:hover {
      color: #333;
      background-color: #e6e6e6;
      border-color: #adadad;
    }
  }
}
</style>
