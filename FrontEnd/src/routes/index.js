import Vue from "vue";
import VueRouter from "vue-router";
import Login from "../views/Signin&Signup/Signin.vue";
import Signup from "../views/Signin&Signup/Signup.vue";
import PaymentComplete from "../views/Order/PaymentComplete.vue";
import Product from "../views/Product/Product.vue";
import RefundRequest from "../views/Refund/RefundRequest.vue";
import Inquiry from "../views/Customer/Inquiry.vue";
import Member from "../views/Member/Member.vue";
import Planning from "../views/Planning&Coupon/Planning.vue";

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
      path: "/paymentComplete",
      name: "PaymentComplete",
      component: PaymentComplete,
    },
    {
      path: "/product",
      name: "Product",
      component: Product,
    },
    {
      path: "/refundRequest",
      name: "RefundRequest",
      component: RefundRequest,
    },
    {
      path: "/inquiry",
      name: "Inquiry",
      component: Inquiry,
    },
    {
      path: "/member",
      name: "Member",
      component: Member,
    },
    {
      path: "/planning",
      name: "Planning",
      component: Planning,
    },
  ],
});
