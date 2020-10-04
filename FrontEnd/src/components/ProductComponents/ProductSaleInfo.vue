<template>
  <section class="product-sale-info">
    <header>
      <span class="header-text">
        <font-awesome-icon class="pencil-icon" icon="pencil-alt" />판매 정보
      </span>
    </header>
    <article>
      <div class="sub-title">
        판매가
        <em>*</em>
      </div>
      <div class="sub-main-col">
        <div class="sale-price-container">
          <input class="sale-price" type="number" v-on:change="price_inputer" />
          <div>
            <span>원</span>
          </div>
        </div>
        <p class="explain">
          <font-awesome-icon
            class="exclamation-icon"
            icon="exclamation-triangle"
          />판매가는 원화기준 10원 이상이며 가격 입력 시 10원 단위로 입력해
          주세요.
        </p>
      </div>
    </article>
    <article>
      <div class="sub-title">할인정보</div>
      <div class="sub-main-col">
        <table>
          <th>할인율</th>
          <th>할인가</th>
          <tr>
            <td>
              <div class="sale-price-container">
                <input
                  class="sale-price"
                  type="number"
                  v-on:change="discount_rate_inputer"
                />
                <div>
                  <span>%</span>
                </div>
              </div>
            </td>
            <td>
              <p>
                <span class="discount-price-num">
                  {{
                    Number(
                      result.body.detail.sale_price *
                        (result.body.detail.discount_rate / 100)
                    ).toLocaleString("en")
                  }} </span
                >원
              </p>
              <button class="discount-button" v-on:click="apply_discount_rate">
                할인판매가적용
              </button>
            </td>
          </tr>
          <tr class="dark-tr">
            <td>할인판매가</td>
            <td>
              <p>
                <span>
                  {{
                    Number(
                      result.body.detail.sale_price *
                        (1 - result.body.detail.discount_rate / 100)
                    ).toLocaleString("en")
                  }} </span
                >원
              </p>
            </td>
          </tr>
          <tr>
            <td>할인기간</td>
            <td>
              <div class="radio">
                <label>
                  <input
                    type="radio"
                    name="discount date"
                    value="false"
                    v-model="discount_term"
                  />무기한
                </label>
                <label>
                  <input
                    type="radio"
                    name="discount date"
                    value="true"
                    v-model="discount_term"
                  />
                  기간설정
                </label>
              </div>

              <div class="date-picker" v-if="discount_term === `true`">
                <datetime
                  type="datetime"
                  class="datetime"
                  format="yyyy-MM-dd HH:mm"
                  v-model="result.body.detail.discount_started_at"
                  :week-start="7"
                  use12-hour
                ></datetime>
                <span class="during-text">~</span>
                <datetime
                  type="datetime"
                  class="datetime"
                  format="yyyy-MM-dd HH:mm"
                  v-model="result.body.detail.discount_ended_at"
                  :min-datetime="result.body.detail.discount_started_at"
                  :week-start="7"
                  use12-hour
                ></datetime>
              </div>
              <p class="red-explain" v-if="discount_term === `true`">
                * 할인기간을 설정시 기간만료되면 자동으로 정상가로 변경 됩니다.
              </p>
            </td>
          </tr>
        </table>

        <p class="explain">
          <font-awesome-icon
            class="exclamation-icon"
            icon="exclamation-triangle"
          />할인판매가 = 판매가 * 할인율
        </p>
        <p class="explain">
          <font-awesome-icon
            class="exclamation-icon"
            icon="exclamation-triangle"
          />할인 판매가 적용 버튼을 클릭 하시면 판매가 정보가 자동
          계산되어집니다.
        </p>
        <p class="explain">
          <font-awesome-icon
            class="exclamation-icon"
            icon="exclamation-triangle"
          />할인 판매가는 원화기준 10원 단위로 자동 반올림됩니다.
        </p>
      </div>
    </article>
    <article>
      <div class="sub-title">최소판매수량</div>
      <div class="sub-main">
        <div class="radio">
          <label v-on:click="at_least_inputer">
            <input
              type="radio"
              name="at least"
              value="1"
              v-model="mininum"
            />1개 이상
          </label>
          <label>
            <input
              type="radio"
              name="at least"
              value="more"
              v-model="mininum"
            />
            <input
              class="amount-limmit"
              type="number"
              v-bind:disabled="mininum == 1"
              v-on:change="at_least_inputer"
            />
            개 이상
          </label>
          <p class="explain">(20개를 초과하여 설정하실 수 없습니다)</p>
        </div>
      </div>
    </article>
    <article>
      <div class="sub-title">최대판매수량</div>
      <div class="sub-main">
        <div class="radio">
          <label v-on:click="maximum_inputer">
            <input
              type="radio"
              name="maximum"
              value="20"
              v-model="maximum"
            />20개
          </label>
          <label>
            <input type="radio" name="maximum" value="less" v-model="maximum" />
            <input
              class="amount-limmit"
              type="number"
              v-bind:disabled="maximum == 20"
              v-on:change="maximum_inputer"
            />
            개 이하
          </label>
          <p class="explain">(20개를 초과하여 설정하실 수 없습니다)</p>
        </div>
      </div>
    </article>
  </section>
</template>

<script>
import DatePicker from "vuejs-datepicker";
import { Datetime } from "vue-datetime";
import "vue-datetime/dist/vue-datetime.css";

export default {
  name: "product-sale-info",
  components: { datetime: Datetime },
  props: [],
  data: () => ({
    spare_discount_rate: "",
    discount_term: "false",
    mininum: 1,
    maximum: 20,
    result: {
      body: {
        detail: {
          sale_price: "",
          discount_rate: "",
          discount_started_at: "",
          discount_ended_at: "",
          minimum_sale_amount: 1,
          maximum_sale_amount: 20,
        },
      },
    },
  }),
  methods: {
    price_inputer: function(e) {
      this.result.body.detail.sale_price = e.target.value;
      this.$emit("sale_price", this.result.body.detail.sale_price);
    },
    discount_rate_inputer: function(e) {
      this.spare_discount_rate = e.target.value;
    },
    apply_discount_rate: function() {
      this.result.body.detail.discount_rate = this.spare_discount_rate;
      this.$emit("discount_rate", this.result.body.detail.discount_rate);
    },
    at_least_inputer: function(e) {
      this.result.body.detail.minimum_sale_amount = e.target.value;
      this.$emit(
        "minimum_sale_amount",
        this.result.body.detail.minimum_sale_amount
      );
    },
    maximum_inputer: function(e) {
      this.result.body.detail.maximum_sale_amount = e.target.value;
      this.$emit(
        "maximum_sale_amount",
        this.result.body.detail.maximum_sale_amount
      );
    },
    input_discount_started_at: function() {
      this.$emit(
        "discount_started_at",
        this.result.body.detail.discount_started_at
      );
    },
    input_discount_ended_at: function() {
      this.$emit(
        "discount_ended_at",
        this.result.body.detail.discount_ended_at
      );
    },
  },
  watch: {
    "result.body.detail.discount_started_at": "input_discount_started_at",
    "result.body.detail.discount_ended_at": "input_discount_ended_at",
  },
};
</script>

<style lang="scss">
.product-sale-info {
  margin: 10px;
  border: 1.3px solid #dddddd;
  border-radius: 5px;

  input:disabled {
    background-color: #eeeeee;
  }

  input:focus,
  button:focus {
    outline: none;
  }

  .explain {
    font-size: 13px;
    color: #1d90ff;
  }

  .red-explain {
    font-size: 13px;
    color: #ff0000;
  }

  .exclamation-icon {
    font-size: 11px;
    margin-right: 3px;
  }

  .radio {
    display: flex;
    align-items: center;
  }

  input[type="radio"] {
    margin-right: 5px;
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

    .header-text {
      position: relative;
      top: 2px;
    }
  }

  em {
    color: #ff0000;
  }

  article {
    display: flex;
    font-size: 13px;
    border-bottom: 1.3px solid #dddddd;
    &:last-child {
      border-bottom: 0;
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

    input[type="radio"] {
      margin-right: 5px;
    }

    label {
      margin-right: 20px;
    }

    .sub-main-col,
    .sub-main {
      display: flex;
      width: 100%;
      font-size: 14px;
      padding: 8px;
    }

    .sale-price-container {
      display: flex;
      overflow: hidden;
      width: 240px;
      border: 1px solid #dddddd;
      border-radius: 5px;
      margin-bottom: 5px;

      .sale-price {
        width: 200px;
        padding: 6px 12px;
        background-color: white;
      }

      div {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 40px;
        border-left: 1px solid #dddddd;
        background-color: #e5e5e5;
      }
    }

    .date-picker {
      display: flex;
      cursor: pointer;

      input[type="text"] {
        border-radius: 3px 0 0 3px;
        text-align: center;
        color: #333333;
        background-color: white;
        border: 1px solid #e5e5e5;
        width: 140px;
        height: 34px;
        padding: 6px 12px;
        cursor: pointer;
        &:focus {
          outline: none;
        }
      }
      .during-text {
        display: inline-block;
        border-color: #e5e5e5;
        background: #e5e5e5;
        min-width: 39px;
        padding: 6px 12px;
        text-align: center;
      }
    }
  }

  input[type="number"] {
    padding: 6px 12px;

    &::-webkit-outer-spin-button,
    &::-webkit-inner-spin-button {
      -webkit-appearance: none;
      margin: 0;
    }
  }

  .amount-limmit {
    height: 34px;
    border: 1px solid #dddddd;
    border-radius: 5px;
    background-color: white;
  }

  table {
    width: 490px;
    height: 255px;
  }
  table,
  th,
  td {
    border: 1px solid #dddddd;
    padding: 8px;
    vertical-align: middle;
  }

  .dark-tr,
  th {
    background-color: #eeeeee;
  }

  .discount-button {
    color: white;
    border: 1px solid #357dbd;
    border-radius: 5px;
    padding: 6px 12px;
    background-color: #438aca;

    &:hover {
      background-color: #3071a8;
    }
  }

  .discount-price-num {
    display: inline-block;
    width: 150px;
  }
}
</style>
