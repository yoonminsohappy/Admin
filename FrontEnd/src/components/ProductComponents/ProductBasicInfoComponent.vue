<template>
  <section class="product-basic-info-component">
    <header>
      <span class="header-text">
        <font-awesome-icon class="pencil-icon" icon="pencil-alt" />기본 정보
      </span>
    </header>
    <article>
      <div class="sub-title">
        <span>
          셀러선택
          <em>*</em>
        </span>
      </div>
      <div class="sub-main">
        <input
          type="text"
          class="seller-search"
          v-bind:value="seller_name_selecter"
          disabled
        />
        <button class="seller-search-button" v-on:click="seller_search_opener">
          셀러검색
        </button>
      </div>
      <div class="search-list">
        <div class="seller-modal-container" v-if="open_seller_search">
          <ul
            v-bind:class="{
              'seller-modal': this.modal_drop,
              'seller-modal-up': !this.modal_drop,
            }"
          >
            <li>
              <span>셀러 선택</span>
            </li>
            <li>
              <p class="explain">
                <font-awesome-icon icon="info-circle" />상품을 등록할 셀러를
                선택해주세요. (검색 10건)
              </p>
              <div class="seller-search-container">
                <div class="serch-title">셀러검색</div>
                <search-list
                  @selected_id="input_select_id"
                  @selected_name="input_select_name"
                />
              </div>
            </li>
            <li>
              <button class="close-button" v-on:click="close_modal">
                닫기
              </button>
              <button
                class="select-seller-button"
                v-on:click="final_seller_select"
              >
                셀러 선택하기
              </button>
            </li>
          </ul>
        </div>
      </div>
    </article>
    <article>
      <div class="sub-title">
        <span>판매여부</span>
      </div>
      <div class="sub-main-col">
        <div class="radio">
          <label>
            <input
              type="radio"
              name="is sold"
              v-on:click="select_sold"
              checked
            />
            <span>판매</span>
          </label>
          <label>
            <input type="radio" name="is sold" v-on:click="select_no_sold" />
            <span>미판매</span>
          </label>
        </div>
        <p class="explain">
          <font-awesome-icon
            class="exclamation-icon"
            icon="exclamation-triangle"
          />미판매 선택시 앱에서 Sold Out으로 표시됩니다.
        </p>
      </div>
    </article>
    <article>
      <div class="sub-title">
        <span>진열여부</span>
      </div>
      <div class="sub-main-col">
        <div class="radio">
          <label>
            <input
              type="radio"
              name="is displayed"
              v-on:click="select_displayed"
              checked
            />
            <span>진열</span>
          </label>
          <label>
            <input
              type="radio"
              name="is displayed"
              v-on:click="select_no_displayed"
            />
            <span>미진열</span>
          </label>
        </div>
        <p class="explain">
          <font-awesome-icon
            class="exclamation-icon"
            icon="exclamation-triangle"
          />미진열 선택시 앱에서 노출되지 않습니다.
        </p>
      </div>
    </article>
    <article>
      <div class="sub-title">
        <span>카테고리</span>
        <em>*</em>
      </div>
      <div class="sub-main">
        <div class="category-container">
          <div class="category-header">
            <span>1차 카테고리</span>
          </div>
          <div class="category-selecter-container">
            <div class="no-seller" v-if="!datas.first_category">
              셀러를 먼저 선택해주세요.
            </div>
            <div class="yes-seller" v-if="datas.first_category">
              <select v-on:change="select_first_category">
                <option>일차 카테고리를 선택해 주세요.</option>
                <option
                  v-for="list in datas.first_category"
                  v-bind:key="list.id"
                  v-bind:value="list.id"
                >
                  {{ list.name }}
                </option>
              </select>
            </div>
          </div>
        </div>
        <div class="category-container">
          <div class="category-header">
            <span>2차 카테고리</span>
          </div>
          <div class="category-selecter-container">
            <div class="no-seller" v-if="!datas.first_category">
              셀러를 먼저 선택해주세요.
            </div>
            <div class="yes-seller" v-if="datas.first_category">
              <select v-on:change="select_second_category">
                <option
                  v-for="list in datas.second_category"
                  v-bind:key="list.id"
                  v-bind:value="list.id"
                >
                  {{ list.name }}
                </option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </article>
    <article>
      <div class="sub-title">
        <span>
          상품 정보 고시
          <em>*</em>
        </span>
      </div>
      <div class="sub-main-col">
        <div class="radio">
          <label v-on:click="details_reference">
            <input type="radio" name="info" checked />
            <span>상품상세 참조</span>
          </label>
          <label v-on:click="origin_self_inputer">
            <input type="radio" name="info" />
            <span>직접입력</span>
          </label>
        </div>
        <ul class="self-input" v-if="open_details_reference">
          <li>
            <div class="self-input-title">제조사(수입사) :</div>
            <div class="self-input-main">
              <input type="text" v-on:change="origin_company_inputer" />
            </div>
          </li>
          <li>
            <div class="self-input-title">제조일자 :</div>
            <div class="self-input-main">
              <datetime
                type="date"
                class="datetime"
                format="yyyy-MM-dd"
                v-model="result.body.detail.origin_date"
                :week-start="7"
                use12-hour
              ></datetime>
            </div>
          </li>
          <li>
            <div class="self-input-title">원산지 :</div>
            <div class="self-input-main">
              <select v-on:change="origin_contry_code_inputer">
                <option
                  v-for="list in datas.contry_list"
                  v-bind:value="list.id"
                  v-bind:key="list.id"
                >
                  {{ list.name }}
                </option>
              </select>
            </div>
          </li>
        </ul>
      </div>
    </article>
    <article>
      <div class="sub-title">
        <span>
          상품명
          <em>*</em>
        </span>
      </div>
      <div class="sub-main-col">
        <input
          class="full-size-input"
          v-on:change="product_name_inputer"
          type="text"
        />
        <p class="explain">
          <font-awesome-icon
            class="exclamation-icon"
            icon="exclamation-triangle"
          />상품명에는 쌍따옴표(") 또는 홑따옴표(')를 포함할 수 없습니다.
        </p>
        <p class="explain">
          <font-awesome-icon
            class="exclamation-icon"
            icon="exclamation-triangle"
          />상품명에는 4byte 이모지를 포함할 수 없습니다.
        </p>
      </div>
    </article>
    <article>
      <div class="sub-title">
        <span>한줄 상품 설명</span>
      </div>
      <div class="sub-main">
        <input
          class="full-size-input"
          v-on:change="simple_description_inputer"
          type="text"
        />
      </div>
    </article>
    <article>
      <div class="sub-title">
        <span>
          이미지 등록
          <em>*</em>
        </span>
      </div>
      <div class="sub-main-col">
        <form>
          <div class="uploading-form">
            <div class="uploading-photo-container">
              <img alt="uploading photo" v-bind:src="image1_Url" />
            </div>
            <label>
              <input
                type="file"
                v-on:change="file_select_image_1"
                ref="image_1"
                accept=".jpg"
              />
              <div class="photo-button">
                <span> <em>*</em>대표 이미지 </span> 선택
              </div>
            </label>
          </div>
          <div class="uploading-form">
            <div class="uploading-photo-container">
              <img alt="uploading photo" v-bind:src="image2_Url" />
            </div>
            <label>
              <input
                type="file"
                v-on:change="file_select_image_2"
                ref="image_2"
                accept=".jpg"
              />
              <div class="photo-button">이미지 선택</div>
            </label>
          </div>
          <div class="uploading-form">
            <div class="uploading-photo-container">
              <img alt="uploading photo" v-bind:src="image3_Url" />
            </div>
            <label>
              <input
                type="file"
                v-on:change="file_select_image_3"
                ref="image_3"
                accept=".jpg"
              />
              <div class="photo-button">이미지 선택</div>
            </label>
          </div>
          <div class="uploading-form">
            <div class="uploading-photo-container">
              <img alt="uploading photo" v-bind:src="image4_Url" />
            </div>
            <label>
              <input
                type="file"
                v-on:change="file_select_image_4"
                ref="image_4"
                accept=".jpg"
              />
              <div class="photo-button">이미지 선택</div>
            </label>
          </div>
          <div class="uploading-form">
            <div class="uploading-photo-container">
              <img alt="uploading photo" v-bind:src="image5_Url" />
            </div>
            <label>
              <input
                type="file"
                v-on:change="file_select_image_5"
                ref="image_5"
                accept=".jpg"
              />
              <div class="photo-button">이미지 선택</div>
            </label>
          </div>
        </form>
        <p class="explain">
          <font-awesome-icon
            class="exclamation-icon"
            icon="exclamation-triangle"
          />640*720사이즈 이상 등록 가능하며 <strong>확장자는 jpg</strong>만
          등록 가능합니다.
        </p>
      </div>
    </article>
    <article>
      <div class="sub-title">
        <span>
          상세 상품 정보
          <em>*</em>
        </span>
      </div>
      <div class="sub-main-col">
        <div class="how-to-upload">
          <label> <input type="radio" checked />간편업로드 </label>
          <p class="explain">
            <font-awesome-icon
              class="exclamation-icon"
              icon="exclamation-triangle"
            />상품 상세이미지의 권장 사이즈는
            <strong>가로사이즈 1000px</strong> 이상입니다.
          </p>
        </div>
        <html-editer @html="upload_description" />
      </div>
    </article>
  </section>
</template>

<script>
import axios from "axios";
import { config } from "../../api/index";
import { Datetime } from "vue-datetime";
import "vue-datetime/dist/vue-datetime.css";
import SearchList from "./SearchList.vue";
import HtmlEditer from "./HtmlEditer.vue";

export default {
  name: "product-basic-info-component",
  components: { SearchList, datetime: Datetime, HtmlEditer },
  props: [],
  data: () => ({
    modal_drop: false,
    open_seller_search: false,
    open_details_reference: false,
    seller_id_selecter: "",
    seller_name_selecter: "셀러 선택을 해주세요",
    make_day: "",
    image1_Url: "https://sadmin.brandi.co.kr/include/img/no_image.png",
    image2_Url: "https://sadmin.brandi.co.kr/include/img/no_image.png",
    image3_Url: "https://sadmin.brandi.co.kr/include/img/no_image.png",
    image4_Url: "https://sadmin.brandi.co.kr/include/img/no_image.png",
    image5_Url: "https://sadmin.brandi.co.kr/include/img/no_image.png",
    datas: {
      first_category: false,
      second_category: [{ name: "일차 카테고리를 먼저 선택해 주세요." }],
      contry_list: [],
    },
    result: {
      image_1: "",
      image_2: "",
      image_3: "",
      image_4: "",
      image_5: "",
      body: {
        product: { first_category: "", second_category: "" },
        detail: {
          is_sold: 1,
          is_displayed: 1,
          origin_company: "",
          origin_date: "",
          country_of_origin_id: "",
          name: "",
          simple_description: "",
          description: "",
        },
      },
    },
  }),
  computed: {},
  methods: {
    seller_search_opener: function () {
      this.open_seller_search = !this.open_seller_search;
      this.modal_drop = !this.modal_drop;
    },
    input_select_id: function (num) {
      this.seller_id_selecter = num;
      this.$emit("seller_id", num);
    },
    input_select_name: function (str) {
      this.seller_name_selecter = str;
    },
    close_modal: function () {
      this.modal_drop = !this.modal_drop;
      setTimeout(() => {
        this.open_seller_search = !this.open_seller_search;
      }, 300);
    },
    final_seller_select: function () {
      axios
        .get(
          `${config}products/first-categories?seller-property-id=${this.seller_id_selecter}`,
          {
            headers: {
              Authorization: localStorage.getItem("access_token"),
            },
          }
        )
        .then((res) => (this.datas.first_category = res.data));

      // axios
      //   .get(
      //     `public/mockdata/seller-property-id=${this.seller_id_selecter}.json`
      //   )
      //   .then((res) => (this.datas.first_category = res.data));

      this.open_seller_search = !this.open_seller_search;
    },
    select_sold: function () {
      this.result.body.detail.is_sold = 1;
      this.$emit("is_sold", this.result.body.detail.is_sold);
    },
    select_no_sold: function () {
      this.result.body.detail.is_sold = 0;
      this.$emit("is_sold", this.result.body.detail.is_sold);
    },
    select_displayed: function () {
      this.result.body.detail.is_displayed = 1;
      this.$emit("is_display", this.result.body.detail.is_displayed);
    },
    select_no_displayed: function () {
      this.result.body.detail.is_displayed = 0;
      this.$emit("is_display", this.result.body.detail.is_displayed);
    },
    select_first_category: function (e) {
      this.result.body.product.first_category = Number(e.target.value);

      axios
        .get(
          `${config}products/second-categories?first-category-id=${e.target.value}`,
          {
            headers: {
              Authorization: localStorage.getItem("access_token"),
            },
          }
        )
        .then((res) => (this.datas.second_category = res.data))
        .then(
          () =>
            (this.result.body.product.second_category = this.datas.second_category[0].id)
        )
        .then(() =>
          this.$emit(
            "second_category_number",
            this.result.body.product.second_category
          )
        );

      this.$emit(
        "first_category_number",
        this.result.body.product.first_category
      );
    },
    select_second_category: function (e) {
      this.result.body.product.second_category = e.target.value;
      this.$emit(
        "second_category_number",
        this.result.body.product.second_category
      );
    },
    details_reference: function () {
      this.open_details_reference = false;
      this.result.body.detail.origin_company = null;
      this.result.body.detail.origin_date = null;
      this.result.body.detail.country_of_origin_id = null;
      this.$emit("reference_off");
    },
    origin_self_inputer: function () {
      this.open_details_reference = true;
      this.result.body.detail.country_of_origin_id = 1;
      this.$emit(
        "input_origin_contry_code",
        this.result.body.detail.country_of_origin_id
      );
    },
    origin_company_inputer: function (e) {
      this.result.body.detail.origin_company = e.target.value;
      this.$emit(
        "input_origin_company",
        this.result.body.detail.origin_company
      );
    },
    origin_date_inputer: function (e) {
      this.$emit("input_origin_date", this.result.body.detail.origin_date);
    },
    origin_contry_code_inputer: function (e) {
      this.result.body.detail.country_of_origin_id = e.target.value;
      this.$emit(
        "input_origin_contry_code",
        this.result.body.detail.country_of_origin_id
      );
    },
    product_name_inputer: function (e) {
      this.result.body.detail.name = e.target.value;
      this.$emit("input_product_name", this.result.body.detail.name);
    },
    simple_description_inputer: function (e) {
      this.result.body.detail.simple_description = e.target.value;
      this.$emit(
        "input_simple_description",
        this.result.body.detail.simple_description
      );
    },
    file_select_image_1: function () {
      this.result.image_1 = this.$refs.image_1.files[0];
      this.image1_Url = URL.createObjectURL(this.result.image_1);
      this.$emit("image_1_file", this.result.image_1);
    },
    file_select_image_2: function () {
      this.result.image_2 = this.$refs.image_2.files[0];
      this.image2_Url = URL.createObjectURL(this.result.image_2);
      this.$emit("image_2_file", this.result.image_2);
    },
    file_select_image_3: function () {
      this.result.image_3 = this.$refs.image_3.files[0];
      this.image3_Url = URL.createObjectURL(this.result.image_3);
      this.$emit("image_3_file", this.result.image_3);
    },
    file_select_image_4: function () {
      this.result.image_4 = this.$refs.image_4.files[0];
      this.image4_Url = URL.createObjectURL(this.result.image_4);
      this.$emit("image_4_file", this.result.image_4);
    },
    file_select_image_5: function () {
      this.result.image_5 = this.$refs.image_5.files[0];
      this.image5_Url = URL.createObjectURL(this.result.image_5);
      this.$emit("image_5_file", this.result.image_5);
    },
    upload_description: function (str) {
      this.result.body.detail.description = str;
      this.$emit("html", str);
    },
  },
  watch: { "result.body.detail.origin_date": "origin_date_inputer" },
  created: function () {
    axios
      .get(`${config}products/countries`, {
        headers: {
          Authorization: localStorage.getItem("access_token"),
        },
      })
      .then((res) => (this.datas.contry_list = res.data));
  },
};
</script>

<style scoped lang="scss">
.product-basic-info-component {
  margin: 10px;
  border: 1.3px solid #dddddd;
  overflow: hidden;
  border-radius: 5px;

  em {
    color: #ff0000;
  }

  input:focus {
    outline: none;
  }

  label {
    input[type="file"] {
      display: none;
    }
  }

  .header-text {
    position: relative;
    top: 2px;
  }

  .seller-modal-container {
    position: fixed;
    z-index: 9999999;
    display: flex;
    justify-content: center;
    align-items: center;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-color: rgba(0, 0, 0, 0.4);

    .seller-modal-up {
      transform: translateY(-70vh);
    }

    .seller-modal {
      animation-name: slidein;

      @keyframes slidein {
        from {
          transform: translateY(-70vh);
        }

        to {
          transform: translateY(0vh);
        }
      }
    }

    .seller-modal-up,
    .seller-modal {
      position: relative;
      width: 500px;
      height: 220px;
      border: 1px solid #4c4c4c;
      border-radius: 10px;
      box-shadow: 2px 2px 10px;
      background-color: #ffffff;
      animation-duration: 0.4s;
      transition: transform 0.4s;

      li {
        border-bottom: 1px solid #dddddd;
        padding: 15px;
        &:first-child {
          display: flex;
          align-items: center;
          height: 56px;
          font-size: 18px;
          font-weight: 300;
        }
        &:last-child {
          display: flex;
          justify-content: flex-end;
          border-bottom: 0;

          button {
            font-size: 14px;
            border-radius: 5px;
            padding: 8px;
          }

          .close-button {
            border: 1px solid #dddddd;

            &:hover {
              background-color: #e6e6e6;
            }
          }

          .select-seller-button {
            color: white;
            border: 1px solid #46b9da;
            margin-left: 10px;
            background-color: #5bc1de;

            &:hover {
              background-color: #2fb1d5;
            }
          }
        }
      }

      .seller-search-container {
        display: flex;
        height: 34px;
        margin-top: 15px;

        .serch-title {
          width: 176px;
          font-size: 14px;
          padding-left: 15px;
        }
      }
    }
  }

  .pencil-icon {
    position: relative;
    bottom: 2px;
    font-size: 11px;
    color: #666666;
  }

  article {
    display: flex;
    font-size: 13px;
    border-bottom: 1.3px solid #dddddd;
    &:last-child {
      border-bottom: 0;
    }
  }

  header {
    display: flex;
    align-items: center;
    height: 38px;
    border-bottom: 1.3px solid #dddddd;
    background-color: #eeeeee;

    span {
      font-size: 16px;
      margin-left: 10px;
    }
  }

  .explain {
    font-size: 13px;
    color: #1d90ff;
  }

  .sub-title {
    display: flex;
    align-items: center;
    width: 15%;
    border-right: 1.3px solid #dddddd;
    padding-left: 10px;
  }

  .sub-main {
    align-items: center;
  }

  .sub-main-col {
    flex-direction: column;
    justify-content: center;
  }

  .radio {
    display: flex;
  }

  .sub-main-col,
  .sub-main {
    display: flex;
    width: 100%;
    font-size: 14px;
    padding: 8px;

    .seller-search {
      width: 20%;
      height: 100%;
      color: black;
      border: 1px solid #dddddd;
      border-radius: 5px;
      padding: 6px 12px;
      background-color: #eeeeee;
    }

    .seller-search-button {
      height: 34px;
      width: 75px;
      color: white;
      border: 1px solid #4cae4c;
      border-radius: 5px;
      padding: 6px 12px;
      margin-left: 10px;
      background-color: #5cb85c;
    }

    .red-explain {
      font-weight: 700;
      color: #ff0000;
    }

    .exclamation-icon {
      font-size: 11px;
      margin-right: 3px;
    }

    label {
      display: flex;
      align-items: center;
      margin-right: 5%;

      input {
        margin-right: 5px;
      }
    }

    .full-size-input {
      width: 100%;
      height: 34px;
      border: 1px solid #dddddd;
      border-radius: 5px;
      padding: 6px 12px;
      background-color: white;
    }
  }

  .self-input {
    margin-top: 15px;

    li {
      display: flex;
      margin-bottom: 5px;

      .self-input-title {
        width: 13%;
      }

      .self-input-main {
        width: 25%;

        input,
        select {
          width: 100%;
          height: 34px;
          border: 1px solid #dddddd;
          background-color: white;
          padding: 6px 12px;
        }
      }
    }
  }

  .category-container {
    width: 50%;
    border: 1px solid #dddddd;

    &:first-child {
      border-right: 0;
    }

    .category-header {
      display: flex;
      align-items: center;
      height: 37px;
      font-weight: 600;
      color: #222222;
      border-bottom: 1px solid #dddddd;
      padding: 8px;
      background-color: white;
    }

    .category-selecter-container {
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 35px;
      border-top: 0;
      padding: 8px;
    }

    .no-seller {
      color: #808080;
    }

    .yes-seller {
      width: 100%;
      border: 1px solid #dddddd;
      background-color: white;

      select {
        width: 100%;
        height: 34px;
        color: #333333;
        padding: 6px 12px;
      }
    }
  }

  form {
    display: flex;
    flex-wrap: wrap;

    .photo-button {
      display: inline-block;
      height: 34px;
      font-size: 13px;
      border: 1px solid #dddddd;
      border-radius: 5px;
      margin-top: 5px;
      padding: 6px 12px;
      background-color: white;

      span {
        color: #1d90ff;
        em {
          font-size: 15px;
          color: inherit;
        }
      }
    }
  }

  .uploading-form {
    display: flex;
    flex-direction: column;
    margin: 5px;

    .uploading-photo-container {
      border: 1px solid #dddddd;
      border-radius: 4px;
      padding: 4px;
      background-color: white;

      img {
        width: 170px;
        height: 170px;
      }
    }
  }

  .how-to-upload {
    width: 98%;
    border-bottom: 1px solid #dddddd;
    margin: 0 10px 20px 10px;

    .explain {
      margin-bottom: 20px;
    }
  }
  .html-maker {
    padding-left: 10px;

    label {
      display: inline-block;
      font-size: 13px;
      border: 1px solid #dddddd;
      border-radius: 5px;
      padding: 6px 12px;
      background-color: white;
    }
  }

  .html-input {
    width: 100%;
    height: 390px;
    border: 1px solid #dddddd;
    border-radius: 5px;
    background-color: white;
  }
}
</style>
