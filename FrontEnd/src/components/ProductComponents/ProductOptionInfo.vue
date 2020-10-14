<template>
  <section class="product-option-info">
    <header>
      <span class="header-text">
        <font-awesome-icon class="pencil-icon" icon="pencil-alt" />옵션 정보
      </span>
    </header>
    <article>
      <div class="sub-title">
        옵션 설정
        <em>*</em>
      </div>
      <div class="sub-main">
        <label> <input type="radio" checked />기본옵션 </label>
      </div>
    </article>
    <article>
      <div class="sub-title">옵션 정보</div>
      <div class="sub-main-col">
        <table>
          <th>옵션항목</th>
          <th>상품옵션명</th>
          <th class="last-th">옵션값 추가/삭제</th>
          <tr v-for="(list, idx) in select_color" v-bind:key="idx + `color`">
            <td v-bind:rowspan="select_color.length" v-if="idx === 0">색상</td>
            <td>
              <div class="option-select-container">
                <div class="option-select-floater">
                  <option-list
                    v-bind:props_list="datas.product_color_list"
                    v-bind:selected_name="list.name"
                    v-bind:idx_num="idx"
                    @selected_content="add_color"
                  />
                </div>
              </div>
            </td>
            <td>
              <button
                class="add"
                v-if="select_color.length > 1"
                v-on:click="delete_color(idx)"
              >
                <font-awesome-icon icon="minus" />
              </button>
              <button class="add" v-on:click="add_color_list">
                <font-awesome-icon icon="plus" />
              </button>
            </td>
          </tr>
          <tr v-for="(list, idx) in select_size" v-bind:key="idx + `size`">
            <td v-bind:rowspan="select_size.length" v-if="idx === 0">사이즈</td>
            <td>
              <div class="option-select-container">
                <div class="option-select-floater">
                  <option-list
                    v-bind:props_list="datas.product_size_list"
                    v-bind:selected_name="list.name"
                    v-bind:idx_num="idx"
                    @selected_content="add_size"
                  />
                </div>
              </div>
            </td>
            <td>
              <button
                class="add"
                v-if="select_size.length > 1"
                v-on:click="delete_size(idx)"
              >
                <font-awesome-icon icon="minus" />
              </button>
              <button class="add" v-on:click="add_size_list">
                <font-awesome-icon icon="plus" />
              </button>
            </td>
          </tr>
          <tr class="stock-manage">
            <td>재고관리여부</td>
            <td colspan="2">
              <div class="radio">
                <label v-on:click="stock_manage_no">
                  <input type="radio" name="Stock manage" checked />재고 수량
                  관리 안함
                </label>
                <label v-on:click="stock_manage_yes">
                  <input type="radio" name="Stock manage" />재고 수량 관리
                </label>
              </div>
            </td>
          </tr>
        </table>

        <button class="option-submit" v-on:click="option_submit">
          <font-awesome-icon icon="check" />적용
        </button>

        <table>
          <tr>
            <th colspan="2">상품옵션정보</th>
            <th rowspan="2">일반재고</th>
            <th rowspan="2" class="minus-th"></th>
          </tr>
          <tr>
            <th class="option-th">색상</th>
            <th class="option-th">사이즈</th>
          </tr>
          <tr
            v-for="(list, idx) in result.body.option"
            v-bind:key="idx + `result`"
          >
            <td>
              <div class="option-select-container">
                <div class="option-select-floater">
                  <option-list
                    v-bind:props_list="datas.product_color_list"
                    v-bind:selected_name="selected_color_name(list.color_id)"
                    v-bind:idx_num="idx"
                    @selected_content="add_color_result"
                  />
                </div>
              </div>
            </td>
            <td>
              <div class="option-select-container">
                <div class="option-select-floater">
                  <option-list
                    v-bind:props_list="datas.product_size_list"
                    v-bind:selected_name="selected_size_name(list.size_id)"
                    v-bind:idx_num="idx"
                    @selected_content="add_size_result"
                  />
                </div>
              </div>
            </td>
            <td>
              <div class="radio">
                <label>
                  <input
                    type="radio"
                    v-bind:name="`common Stock` + list.color_id + list.size_id"
                    value="false"
                    v-model="list.is_stock_manage"
                  />재고관리안함
                </label>
                <label>
                  <input
                    type="radio"
                    v-bind:name="`common Stock` + list.color_id + list.size_id"
                    value="true"
                    v-model="list.is_stock_manage"
                  />
                  <input
                    type="number"
                    class="stock-input"
                    v-bind:disabled="list.is_stock_manage === `false`"
                    v-on:change="stock_inputer_change"
                    v-on:focusout="stock_inputer(idx)"
                  />
                  개
                </label>
              </div>
            </td>
            <td>
              <button class="minus" v-on:click="delete_result(idx)">
                <font-awesome-icon icon="minus" />
              </button>
            </td>
          </tr>
        </table>

        <p class="explain">
          <font-awesome-icon
            class="exclamation-icon"
            icon="exclamation-triangle"
          />도매처옵션명 조합은 최대 100자까지 표시됩니다.
        </p>
      </div>
    </article>
  </section>
</template>

<script>
import axios from "axios";
import { config } from "../../api/index";
import OptionList from "./OptionList";

export default {
  name: "product-option-info",
  components: { OptionList },
  props: [],
  data: () => ({
    stock_manage: "false",
    typing_stock: "",
    select_color: [{ id: "", name: "색상 옵션을 선택해 주세요." }],
    select_size: [{ id: "", name: "사이즈 옵션을 선택해 주세요." }],
    datas: { product_color_list: [], product_size_list: [] },
    result: {
      body: {
        option: [],
      },
    },
  }),
  methods: {
    option_submit: function () {
      let Arr = [];
      for (let i in this.select_color) {
        if (!this.select_color[i].id) {
          return alert("색상을 선택해 주세요.");
        }
      }

      for (let i in this.select_size) {
        if (!this.select_size[i].id) {
          return alert("사이즈를 선택해 주세요.");
        }
      }

      for (let x in this.select_color) {
        for (let y in this.select_size) {
          Arr.push({
            color_id: this.select_color[x].id,
            size_id: this.select_size[y].id,
            stock: "",
            is_stock_manage: this.stock_manage,
          });
        }
      }

      this.result.body.option = Arr;

      this.$emit("option", Arr);
    },
    delete_color: function (idx) {
      this.select_color.splice(idx, 1);
    },
    add_color: function (obj) {
      for (let i in this.select_color) {
        if (this.select_color[i].name === obj.name) {
          return alert("이미 선택된 옵션입니다.");
        }
      }
      this.$set(this.select_color, obj.idx, { id: obj.id, name: obj.name });
    },
    add_color_list: function () {
      this.select_color.push({
        id: "",
        name: "색상 옵션을 선택해 주세요.",
      });
    },
    delete_size: function (idx) {
      this.select_size.splice(idx, 1);
    },
    add_size: function (obj) {
      for (let i in this.select_size) {
        if (this.select_size[i].name === obj.name) {
          return alert("이미 선택된 옵션입니다.");
        }
      }
      this.$set(this.select_size, obj.idx, { id: obj.id, name: obj.name });
    },
    add_size_list: function () {
      this.select_size.push({
        id: "",
        name: "사이즈 옵션을 선택해 주세요.",
      });
    },
    stock_manage_yes: function () {
      this.stock_manage = true;
    },
    stock_manage_no: function () {
      this.stock_manage = false;
    },
    delete_result: function (idx) {
      this.result.body.option.splice(idx, 1);
      this.$emit("delete", idx);
    },

    add_color_result: function (obj) {
      this.$set(this.result.body.option[obj.idx], "color_id", obj.id);
      this.$emit("modify_color_result", obj);
    },
    add_size_result: function (obj) {
      this.$set(this.result.body.option[obj.idx], "size_id", obj.id);
      this.$emit("modify_size_result", obj);
    },
    stock_inputer_change: function (e) {
      this.typing_stock = e.target.value;
    },
    stock_inputer: function (idx) {
      this.result.body.option[idx].stock = this.typing_stock;
      this.$emit("stock", this.result.body.option);
    },
    selected_color_name: function (num) {
      for (let i in this.datas.product_color_list) {
        if (this.datas.product_color_list[i].id === num) {
          return this.datas.product_color_list[i].name;
        }
      }
    },
    selected_size_name: function (num) {
      for (let i in this.datas.product_size_list) {
        if (this.datas.product_size_list[i].id === num) {
          return this.datas.product_size_list[i].name;
        }
      }
    },
  },
  created: function () {
    axios
      .get(`${config}products/colors`, {
        headers: {
          Authorization: localStorage.getItem("access_token"),
        },
      })
      .then((res) => (this.datas.product_color_list = res.data));
    axios
      .get(`${config}products/sizes`, {
        headers: {
          Authorization: localStorage.getItem("access_token"),
        },
      })
      .then((res) => (this.datas.product_size_list = res.data));
    // axios
    //   .get(`public/mockdata/product_color.json`)
    //   .then((res) => (this.datas.product_color_list = res.data));
    // axios
    //   .get(`public/mockdata/product_size.json`)
    //   .then((res) => (this.datas.product_size_list = res.data));
  },
};
</script>

<style lang="scss">
.product-option-info {
  margin: 10px;
  border: 1.3px solid #dddddd;
  border-radius: 5px;

  input[type="number"] {
    &::-webkit-outer-spin-button,
    &::-webkit-inner-spin-button {
      -webkit-appearance: none;
      margin: 0;
    }
  }

  input:disabled {
    background-color: #eeeeee;
  }

  input:focus,
  button:focus {
    outline: none;
  }

  .option-select-container {
    position: relative;
    width: 100%;
    height: 39px;

    .option-select-floater {
      position: absolute;
      width: 100%;
      top: 0%;
      left: 0;
    }
  }

  .explain {
    font-size: 13px;
    color: #1d90ff;
  }

  .exclamation-icon {
    font-size: 11px;
    margin-right: 3px;
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
      align-items: center;
    }

    input[type="radio"] {
      margin-right: 5px;
    }

    label {
      display: flex;
      align-items: center;
      margin-right: 20px;
    }

    .sub-main-col,
    .sub-main {
      display: flex;
      width: 100%;
      font-size: 14px;
      padding: 8px;
    }

    .add {
      display: inline-block;
      border: 1px solid #dddddd;
      border-radius: 5px;
      padding: 8px;
    }

    .minus {
      display: inline-block;
      color: white;
      border-radius: 5px;
      padding: 8px 12px;
      background-color: #d8544f;
    }

    .last-th {
      width: 150px;
    }

    .option-submit {
      width: 64px;
      height: 30px;
      color: white;
      white-space: nowrap;
      border: 1px solid #46b9da;
      border-radius: 5px;
      margin: 10px 0;
      padding: 5px 10px;
      background-color: #5bc1de;

      &:hover {
        background-color: #2fb1d5;
      }
    }

    table,
    th,
    td {
      border: 1px solid #dddddd;
      padding: 8px;
      vertical-align: middle;
      text-align: center;
    }

    th,
    .stock-manage {
      background-color: #eeeeee;
    }

    th {
      height: 37px;
      font-size: 14px;
      font-weight: 600;
    }
  }

  .color-pick {
    border: 1px solid #dddddd;
    border-radius: 5px;
  }

  .stock-input {
    width: 100px;
    height: 34px;
    border: 1px solid #dddddd;
    border-radius: 5px;
    background-color: white;
    padding: 6px 12px;
    margin-right: 10px;
  }

  .minus-th {
    width: 100px;
  }

  .option-th {
    width: 20%;
  }
}
</style>
