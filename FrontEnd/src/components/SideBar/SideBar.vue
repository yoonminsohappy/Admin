<template>
  <div class="page-side-bar">
    <ul class="page-side-menu">
      <li class="toggle-btn">
        <font-awesome-icon class="toggle-icon" icon="angle-left" />
      </li>
      <li class="side-menu-list" v-for="menu in menuList" v-bind:key="menu.id">
        <side-bar-list :sideMenuList="menu"></side-bar-list>
      </li>
    </ul>
  </div>
</template>

<script>
import SideBarList from "./Components/SideBarList";

export default {
  data: function() {
    return {
      menuList: [
        {
          name: "주문관리",
          icon: "cart-arrow-down",
          id: 1,
          openMenuList: [
            { name: "결제완료관리", url: "/order/paymentComplete" },
            { name: "상품준비관리", url: "/order/productPrepare" },
            { name: "배송중관리", url: "/order/delivery" },
            { name: "배송완료관리", url: "/order/deliveryComplete" },
          ],
        },
        {
          name: "취소/환불 관리",
          icon: "shopping-cart",
          id: 2,
          openMenuList: [
            { name: "환불요청관리", url: "/refundRequest" },
            { name: "환불완료관리", url: "/refundComplete" },
            { name: "주문취소완료관리", url: "/cancelComplete" },
          ],
        },
        {
          name: "상품관리",
          icon: "shopping-bag",
          id: 3,
          openMenuList: [
            { name: "상품 관리", url: "/product" },
            { name: "상품 등록", url: "/productRegist" },
          ],
        },
        {
          name: "고객응대관리",
          icon: "smile",
          id: 4,
          openMenuList: [
            { name: "Q&A 관리", url: "/inquiry" },
            { name: "텍스트 리뷰", url: "/textReview" },
          ],
        },
        {
          name: "기획전/쿠폰관리",
          icon: "gift",
          id: 5,
          openMenuList: [
            { name: "기획전 관리", url: "/planning" },
            { name: "쿠폰 관리", url: "/coupon" },
          ],
        },
        {
          name: "회원관리",
          icon: "user",
          id: 6,
          openMenuList: [
            { name: "회원 관리_커뮤니티", url: "/member" },
            { name: "셀러 계정 관리", url: "/account" },
          ],
        },
      ],
    };
  },
  components: { SideBarList },
};
</script>

<style lang="scss" scoped>
.page-side-bar {
  margin-top: 45px;
  min-width: 215px;
  min-height: 651px;
  background-color: #35363a;

  .page-side-menu {
    .toggle-btn {
      border: 0;
      border-bottom: 1px solid transparent;
      padding: 0;
      margin: 0;
      display: flex;
      align-items: center;
      justify-content: flex-end;
      cursor: default;

      &:hover {
        background-color: #35363a;
      }
    }

    .toggle-icon {
      margin: 15px -1px 15px 0;
      width: 24px;
      height: 23px;
      background-color: #fcfcfc;
      border-radius: 4px 0px 0px 4px;
      cursor: pointer;
    }

    .side-menu-list {
      cursor: pointer;
    }
  }
}
// @media (min-width: 1000px) and (max-width: 1500px) {
//   .page-side-bar {
//     min-height: 699px;
//   }
// }
</style>
