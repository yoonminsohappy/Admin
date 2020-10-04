<template>
  <div class="page-bar">
    <ul class="bar-list">
      <i class="fa fa-list arrow"></i>
      <li>
        주문관리
        <font-awesome-icon class="arrow-icon" icon="angle-left" />
      </li>
      <li>
        결제완료 관리
        <font-awesome-icon class="arrow-icon" icon="angle-left" />
      </li>
      <li>결제완료 리스트</li>
    </ul>
    <div class="list-order-filter">
      <div class="filter-area">
        <div class="select-area">
          <select name="filterOrder" id="filterOrder" class="filter-select">
            <option value="NEW">최신주문일</option>
            <option value="OLD">주문일의 역순</option>
          </select>
          <font-awesome-icon class="select-arrow" icon="angle-left" />
        </div>
        <div class="select-area">
          <select
            v-model="limit"
            @change="fetchFilter"
            name="filterLimit"
            id="filterLimit"
            class="filter-select"
          >
            <option value="10">10개씩보기</option>
            <option value="20">20개씩보기</option>
            <option value="50" selected="selected">50개씩보기</option>
            <option value="100">100개씩보기</option>
            <option value="150">150개씩보기</option>
          </select>
          <font-awesome-icon class="select-arrow" icon="angle-left" />
        </div>
      </div>
      <div class="filter-area">
        <select name="filterLimit" id="filterLimit"></select>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";

export default {
  computed: {
    ...mapGetters("order", ["LimitData"]),
    limit: {
      get() {
        return this.LimitData;
      },
      set(value) {
        this.setLimit(value);
      },
    },
  },
  methods: {
    ...mapActions("order", ["fetchFilter", "setLimit"]),
  },
};
</script>

<style scoped lang="scss">
.page-bar {
  display: flex;
  justify-content: space-between;
  background-color: #eee;
  margin: 0 -20px 10px -20px;
  padding: 0 20px 0 10px;
  font-size: 13px;
  .bar-list {
    padding: 8px;
    display: flex;
    align-items: center;
    justify-content: flex-start;
    .arrow {
      margin-right: 5px;
    }
    .arrow-icon {
      color: #999;
      font-size: 14px;
      width: 1.25em;
      transform: rotate(-180deg);
    }
  }
  .list-order-filter {
    display: flex;
    .filter-area {
      display: flex;
      align-items: center;
      .select-area {
        position: relative;
        .filter-select {
          height: 30px;
          line-height: 28px;
          padding: 2px 10px;
          font-size: 13px;
          width: 120px !important;
          background-color: white;
          border: 1px solid #e5e5e5;
          border-radius: 4px;
          &:focus {
            border-color: #999999;
            outline: 0;
          }
        }
        .select-arrow {
          position: absolute;
          right: 10%;
          top: 35%;
          transform: rotate(-90deg);
        }
      }
    }
  }
}
</style>
