<template>
  <div class="product-regist">
    <header>
      <h1>
        상품 등록
        <span>상품 정보 등록</span>
      </h1>
      <ul class="sub-nav">
        <li>
          <font-awesome-icon class="home-icon" icon="home" />
        </li>
        <li>
          상품관리
          <span>></span>
        </li>
        <li>
          상품 관리
          <span>></span>
        </li>
        <li>상품 등록</li>
      </ul>
    </header>
    <main>
      <product-basic-info-component
        @seller_id="seller_id_changer"
        @is_sold="sold_selecter"
        @is_display="display_selecter"
        @first_category_number="first_category_number_changer"
        @second_category_number="second_category_number_changer"
        @reference_off="reference_close"
        @input_origin_company="origin_company_changer"
        @input_origin_date="origin_date_changer"
        @input_origin_contry_code="origin_contry_code_changer"
        @input_product_name="product_name_changer"
        @input_simple_description="simple_description_changer"
        @html="input_html"
        @image_1_file="input_image_1"
        @image_2_file="input_image_2"
        @image_3_file="input_image_3"
        @image_4_file="input_image_4"
        @image_5_file="input_image_5"
      />
      <product-option-info
        @option="input_option"
        @modify_color_result="modify_color_result_list"
        @modify_size_result="modify_size_result_list"
        @stock="modify_stock"
      />
      <product-sale-info
        @sale_price="input_sale_price"
        @discount_rate="input_discount_rate"
        @minimum_sale_amount="input_minimum_sale_amount"
        @maximum_sale_amount="input_maximum_sale_amount"
        @discount_started_at="input_discount_started_at"
        @discount_ended_at="input_discount_ended_at"
      />
      <section class="submit-container">
        <button class="submit" v-on:click="submit">등록</button>
        <button class="cencle">취소</button>
      </section>
    </main>
  </div>
</template>

<script>
import axios from "axios";
import { config } from "../../api/index";
import ProductBasicInfoComponent from "../../components/ProductComponents/ProductBasicInfoComponent.vue";
import ProductOptionInfo from "../../components/ProductComponents/ProductOptionInfo.vue";
import ProductSaleInfo from "../../components/ProductComponents/ProductSaleInfo.vue";

export default {
  name: "product-regist",
  components: { ProductBasicInfoComponent, ProductOptionInfo, ProductSaleInfo },
  props: [],
  data: () => ({
    result: {
      image_1: "",
      image_2: "",
      image_3: "",
      image_4: "",
      image_5: "",
      body: {
        product: {
          first_category_id: "",
          second_category_id: "",
          seller_id: "",
        },
        detail: {
          is_sold: 1,
          is_displayed: 1,
          origin_company: null,
          origin_date: null,
          country_of_origin_id: null,
          name: "",
          simple_description: null,
          description: "",
          sale_price: "",
          discount_rate: "",
          discount_started_at: "",
          discount_ended_at: "",
          minimum_sale_amount: 1,
          maximum_sale_amount: 20,
        },
        options: [{ stock: "", color_id: "", size_id: "" }],
      },
    },
  }),
  computed: {},

  methods: {
    input_sale_price: function (num) {
      this.result.body.detail.sale_price = num;
    },
    seller_id_changer: function (num) {
      this.result.body.product.seller_id = num;
    },
    input_discount_rate: function (num) {
      this.result.body.detail.discount_rate = num;
    },
    input_minimum_sale_amount: function (num) {
      this.result.body.detail.minimum_sale_amount = Number(num);
    },
    input_maximum_sale_amount: function (num) {
      this.result.body.detail.maximum_sale_amount = Number(num);
    },
    input_discount_started_at: function (str) {
      this.result.body.detail.discount_started_at =
        str.slice(0, 10) + ` ` + str.slice(11, 19);
    },
    input_discount_ended_at: function (str) {
      this.result.body.detail.discount_ended_at =
        str.slice(0, 10) + ` ` + str.slice(11, 19);
    },
    input_option: function (arr) {
      this.result.body.options = arr;
    },
    modify_color_result_list: function (obj) {
      this.$set(this.result.body.options[obj.idx], "color_id", obj.id);
    },
    modify_size_result_list: function (obj) {
      this.$set(this.result.body.options[obj.idx], "size_id", obj.id);
    },
    sold_selecter: function (num) {
      this.result.body.detail.is_sold = num;
    },
    display_selecter: function (num) {
      this.result.body.detail.is_displayed = num;
    },
    first_category_number_changer: function (num) {
      this.result.body.product.first_category_id = num;
    },
    second_category_number_changer: function (num) {
      this.result.body.product.second_category_id = Number(num);
    },
    reference_close: function () {
      this.result.body.detail.origin_company = null;
      this.result.body.detail.origin_date = null;
      this.result.body.detail.country_of_origin_id = null;
    },
    origin_company_changer: function (str) {
      this.result.body.detail.origin_company = str;
    },
    origin_date_changer: function (str) {
      if (str === null) {
        this.result.body.detail.origin_date = str;
      } else {
        this.result.body.detail.origin_date = str.slice(0, 10);
      }
    },
    origin_contry_code_changer: function (str) {
      this.result.body.detail.country_of_origin_id = str;
    },
    product_name_changer: function (str) {
      this.result.body.detail.name = str;
    },
    simple_description_changer: function (str) {
      this.result.body.detail.simple_description = str;
    },
    input_image_1: function (obj) {
      this.result.image_1 = obj;
    },
    input_image_2: function (obj) {
      this.result.image_2 = obj;
    },
    input_image_3: function (obj) {
      this.result.image_3 = obj;
    },
    input_image_4: function (obj) {
      this.result.image_4 = obj;
    },
    input_image_5: function (obj) {
      this.result.image_5 = obj;
    },
    input_html: function (str) {
      this.result.body.detail.description = str;
    },
    modify_stock: function (arr) {
      this.result.body.options = arr;
    },

    submit: function () {
      const form_data = new FormData();
      form_data.append("image_1", this.result.image_1);
      form_data.append("image_2", this.result.image_2);
      form_data.append("image_3", this.result.image_3);
      form_data.append("image_4", this.result.image_4);
      form_data.append("image_5", this.result.image_5);
      form_data.append("body", JSON.stringify(this.result.body));

      axios
        .post(`${config}products`, form_data, {
          header: {
            "content-Type": "mutipart/from-data",
            Authorization: localStorage.getItem("access_token"),
          },
        })
        .then((res) => console.log(res))
        .catch((err) => console.log(err));
    },
  },
};
</script>

<style lang="scss" scoped>
.product-regist {
  background-color: #fafafa;
  padding-top: 45px;

  .home-icon {
    position: relative;
    top: -1px;
    font-size: 11px;
    color: #999999;
    margin-right: 5px;
  }

  p {
    margin: 0;
  }

  h1 {
    font-size: 26px;
    font-weight: 300;
    padding-top: 25px;
    padding-left: 20px;

    span {
      font-size: 13px;
      margin-left: 7px;
    }
  }

  .sub-nav {
    display: flex;
    align-items: center;
    height: 34px;
    padding-left: 20px;
    background-color: #eeeeee;

    li {
      display: flex;
      align-items: center;
      font-size: 13px;

      span {
        font-size: 8px;
        color: #999999;
        margin: 0 5px;
      }
    }
  }

  .submit-container {
    display: flex;
    justify-content: center;
    padding: 30px 0;

    .submit,
    .cencle {
      width: 50px;
      height: 34px;
      font-size: 14px;
      color: white;
      border-radius: 5px;
      opacity: 0.8;
      padding: 8px;

      &:hover {
        opacity: 1;
      }
    }

    .submit {
      background-color: #449d44;
      margin-right: 10px;
    }

    .cencle {
      background-color: #c9312c;
    }
  }
}
</style>
