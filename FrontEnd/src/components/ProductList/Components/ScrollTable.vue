<template>
  <div class="scroll-table">
    <table class="table">
      <thead>
        <tr role="row" class="heading">
          <th>
            <div class="checker">
              <span><input class="groupCheckable" type="checkbox"/></span>
            </div>
          </th>
          <th v-for="(item, index) in tableHeader" :key="index">
            {{ item }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="filter === undefined"></tr>
        <tr v-else-if="!filter.length">
          <th colspan="13" class="empty">조회된 데이터가 없습니다.</th>
        </tr>
        <tr v-else v-for="(item, index) in filter" :key="index">
          <th>
            <div class="checker">
              <span
                ><input
                  class="groupCheckable"
                  type="checkbox"
                  @change="clickCheck"
              /></span>
            </div>
          </th>
          <th>{{ item.payment_complete }}</th>
          <th>{{ item.order_number }}</th>
          <th>
            <a href="#">{{ item.order_detail_number }}</a>
          </th>
          <th>{{ item.seller_name }}</th>
          <th>{{ item.product_name }}</th>
          <th>{{ item.option_info }}</th>
          <th>{{ item.quantity }}</th>
          <th>{{ item.user_name }}</th>
          <th>{{ item.phone_number }}</th>
          <th>{{ item.final_price }}</th>
          <th>0</th>
          <th>결제완료</th>
        </tr>
      </tbody>
      <tfoot></tfoot>
    </table>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
export default {
  computed: {
    ...mapGetters("order", ["filterData"]),
    filter() {
      return this.filterData.order_data;
    },
  },
  data() {
    return {
      tableHeader: [
        "결제일자",
        "주문번호",
        "주문상세번호",
        "셀러명",
        "상품명",
        "옵션정보",
        "수량",
        "주문자명",
        "핸드폰번호",
        "결제금액",
        "쿠폰할인",
        "주문상태",
      ],
      isClicked: false,
    };
  },
  methods: {
    clickCheck(e) {
      let isClicked = e.target.checked;
      this.isClicked = isClicked;
    },
  },
};
</script>

<style scoped lang="scss">
.scroll-table {
  width: 100%;
  overflow-x: auto;
  overflow-y: hidden;
  border: 1px solid #dddddd;
  margin: 10px 0 !important;
  font-size: 13px;

  .table {
    border: 0;
    width: 100% !important;
    background-color: #fff;

    .empty {
      background-color: #f9f9f9;
      white-space: nowrap;
      text-align: center;
    }

    tr.heading > th {
      white-space: nowrap;
      background-color: #eee !important;
      font-size: 14px;
      font-weight: 600;
      border: 1px solid #ddd;
      padding: 8px;
    }

    .table-scrollable > .table > thead > tr > th {
      white-space: nowrap;
      font-size: 14px;
      padding: 8px;
      border: 1px solid #ddd;
      font-weight: 600;
    }
    th {
      white-space: nowrap;
      text-align: left;
      border: 1px solid #ddd;
    }
  }
}
</style>
