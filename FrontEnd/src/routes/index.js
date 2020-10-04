import Vue from "vue";
import VueRouter from "vue-router";
import Login from "../views/Signin&Signup/Signin.vue";
import Signup from "../views/Signin&Signup/Signup.vue";
import Order from "../views/Order/Order.vue";
import RefundRequest from "../views/Refund/RefundRequest.vue";
import RefundComplete from "../views/Refund/RefundCompleteList.vue";
import CancelComplete from "../views/Refund/CancelCompleteList.vue";
import Product from "../views/Product/Product.vue";
import ProductRegist from "../views/Product/ProductRegist.vue";
import Inquiry from "../views/Customer/InquiryList.vue";
import TextReview from "../views/Customer/TextReviewList.vue";
import Planning from "../views/Planning&Coupon/Planning.vue";
import Coupon from "../views/Planning&Coupon/Coupon.vue";
import Member from "../views/Member/Member.vue";
import Account from "../views/Member/Account.vue";
import SideBar from "../components/SideBar/SideBar"

import Nav from "../components/Nav/Nav.vue"

Vue.use(VueRouter);

export const router = new VueRouter({
  mode: "history",
  routes: [
    {
      path: "/",
      name: "Login",
      component: Login,
    },
    {
      path: "/signup",
      name: "Signup",
      component: Signup,
    },
    {
      path: "/order/:id",
      name: "Order",
      component: Order,
      props:true
    },
    {
      path: "/product",
      name: "Product",
      component: Product,
    },
    {
      path: "/productRegist",
      name: "ProductRegist",
      component: ProductRegist,
    },
    {
      path: "/refundRequest",
      name: "RefundRequest",
      component: RefundRequest,
    },
    {
      path: "/refundComplete",
      name: "RefundComplete",
      component: RefundComplete,
    },
    {
      path: "/cancelComplete",
      name: "CancelComplete",
      component: CancelComplete,
    },
    {
      path: "/inquiry",
      name: "Inquiry",
      component: Inquiry,
    },
    {
      path: "/textReview",
      name: "TextReview",
      component: TextReview,
    },
    {
      path: "/member",
      name: "Member",
      component: Member,
    },
    {
      path: "/account",
      name: "Account",
      component: Account,
    },
    {
      path: "/planning",
      name: "Planning",
      component: Planning,
    },
    {
      path: "/coupon",
      name: "Coupon",
      component: Coupon,
    },
    {
      path: "/sideBar",
      name: "SideBar",
      component: SideBar,
    },
  ],
});
