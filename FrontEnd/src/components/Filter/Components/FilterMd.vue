<template>
  <div class="seller-md">
    <div class="md-title">
      <label class="md-text"> 셀러속성 : </label>
    </div>
    <div class="md-btn-list">
      <button
        v-for="mdVal of mdList"
        :key="mdVal.key"
        @click="clickBtn(mdVal.key)"
        :class="{ 'clicked-btn': isChecked(mdVal.key) }"
        class="md-btn"
      >
        {{ mdVal.name }}
      </button>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapMutations } from "vuex";
export default {
  data() {
    return {
      mdList: [
        { key: 0, name: "전체" },
        { key: 1, name: "쇼핑몰" },
        { key: 2, name: "마켓" },
        { key: 3, name: "로드샵" },
        { key: 4, name: "디자이너브랜드" },
        { key: 5, name: "제너럴 브랜드" },
        { key: 6, name: "내셔럴 브랜드" },
        { key: 7, name: "뷰티" },
      ],
    };
  },
  computed: {
    ...mapGetters("order", ["mdValues"]),
    md() {
      return this.mdValues;
    },
  },
  methods: {
    ...mapMutations("order", ["setMdValues"]),
    clickBtn(key) {
      let arr = [];
      if (key > 0) {
        arr = [...this.md];
        //이미 값이 있는 경우에는 값을 빼기
        if (arr.includes(key)) {
          let idx = arr.indexOf(key);
          arr.splice(idx, 1);
        }
        //새로운 값일 경우에는 값을 넣기
        else if (!arr.includes(key)) {
          arr = [...arr, key];
        }
      }
      //새로 만든 배열의 길이가 0이거나 7일 때는 다시 빈배열 []
      if (arr.length === 0 || arr.length === this.mdList.length - 1) {
        arr = [];
      }
      this.setMdValues(arr.sort((a, b) => a - b));
    },
    isChecked(value) {
      if (this.md.length === 0 && value === 0) return true;
      return this.md.includes(value);
    },
  },
};
</script>

<style scoped lang="scss">
.seller-md {
  display: flex;
  margin-bottom: 10px;
  padding: 0 15px;
  font-size: 13px;

  .md-title {
    width: 125px;
    .md-text {
      padding-top: 7px;
      height: 30px;
      font-weight: 400;
      font-size: 14px;
      max-width: 100%;
      margin-bottom: 5px;
    }
  }
  .md-btn-list {
    min-height: 1px;
    padding-right: 15px;
    .md-btn {
      margin-right: 3px;
      color: #333;
      background-color: #fff;
      border: 1px solid transparent;
      border-color: #e5e5e5;
      border-radius: 4px;
      padding: 6px 12px;
      font-size: 14px;
      &:focus {
        outline: none !important;
      }
      &:hover {
        color: #333;
        background-color: #e6e6e6;
        border-color: #adadad;
      }
    }
    .clicked-btn {
      background-color: #428bca;
      color: white;
      &:hover {
        background-color: #428bca;
        color: white;
        border-color: #adadad;
      }
    }
  }
}
</style>
