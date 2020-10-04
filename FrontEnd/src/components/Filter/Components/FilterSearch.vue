<template>
  <div class="input-area">
    <div class="select">
      <select @change="optName" class="select-box">
        <optgroup
          v-for="(data, index) in optdata"
          :key="index"
          :label="data.label"
        >
          <option v-for="(item, index) in data.name" :key="index">
            {{ item }}
          </option>
        </optgroup>
      </select>
      <font-awesome-icon class="arrow-icon" icon="angle-left" />
    </div>
    <div class="search-box">
      <input
        type="text"
        class="search-input"
        placeholder="검색어를 입력하세요."
        @change="searchText"
      />
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      optdata: [
        { name: ["Select..", "주문번호", "주문상세번호"] },
        { name: ["주문자명", "핸드폰번호"], label: "----------------" },
        { name: ["셀러명", "상품명"], label: "----------------" },
      ],
    };
  },
  methods: {
    optName(e) {
      let optName = e.target.value;
      this.$store.commit("order/setOptName", optName);
    },
    searchText(e) {
      let text = e.target.value;
      this.$store.commit("order/setText", text);
    },
  },
};
</script>

<style scoped lang="scss">
.input-area {
  display: flex;
  margin: 10px 0;
  width: 100%;
  padding: 0 15px;

  .select {
    position: relative;
    margin-right: 5px;

    .select-box {
      height: 30px;
      line-height: 28px;
      padding: 0 10px;
      border: 1px solid #e5e5e5;
      border-radius: 4px;
      font-size: 13px;
      width: 120px;
      vertical-align: middle;
      &:focus {
        outline: none;
      }
    }
    .arrow-icon {
      position: absolute;
      top: 25%;
      right: 10px;
      transform: rotate(-90deg);
    }
  }

  .search-box {
    width: 33.33333333%;
    min-height: 1px;
    padding-right: 15px;

    .search-input {
      height: 30px;
      width: 100%;
      padding: 6px 10px;
      font-size: 13px;
      border: 1px solid #ccc;
      border-radius: 3px;

      &:focus {
        border-color: #999999;
        outline: 0;
      }
    }
  }
}
</style>
