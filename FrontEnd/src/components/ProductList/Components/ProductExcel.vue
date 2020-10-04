<template>
  <div class="product-excel">
    <div class="product">
      <div class="text">전체 조회건 수 : {{ filterData.count }}건</div>
      <button class="product-btn">주문취소처리</button>
    </div>
    <div class="excel-btn">
      <button>
        <i class="fa fa-file-excel-o mg-r-2"></i>
        전체주문 엑셀다운로드
      </button>
      <button>
        <i class="fa fa-file-excel-o mg-r-2"></i>
        선택주문 엑셀다운로드
      </button>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
export default {
  computed: {
    ...mapGetters("order", ["filterData"]),
  },
};
</script>

<style scoped lang="scss">
.product-excel {
  width: 100%;
  color: #222222;
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  .product {
    display: flex;
    .product-btn {
      margin-left: 20px;
      padding: 1px 5px;
      font-size: 12px;
      line-height: 1.5;
      font-weight: bold;
      border-radius: 3px;
      color: #fff;
      background-color: #428bca;
      border-color: #357ebd;
      outline: none !important;

      &:hover {
        color: #fff;
        background-color: #3071a9;
        border-color: #285e8e;
      }
    }
  }
  .excel-btn {
    button {
      padding: 1px 5px;
      font-size: 12px;
      line-height: 1.5;
      font-weight: bold;
      border-radius: 3px;
      color: #fff;
      background-color: #5cb85c;
      border-color: #4cae4c;
      outline: none !important;

      &:hover {
        color: #fff;
        background-color: #449d44;
        border-color: #398439;
      }
    }
  }
}
</style>
