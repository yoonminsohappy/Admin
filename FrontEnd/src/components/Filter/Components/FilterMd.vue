<template>
  <div class="seller-md">
    <div class="md-title">
      <label class="md-text">
        셀러속성 :
      </label>
    </div>
    <div class="md-btn-list">
      <button
        v-for="(md, index) in mdList"
        :key="index"
        @click="clickBtn({ md, index })"
        :class="{ 'clicked-btn': md.isClicked }"
        class="md-btn"
      >
        {{ md.name }}
      </button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      mdList: [
        { name: "전체", isClicked: true },
        { name: "쇼핑몰", isClicked: false },
        { name: "마켓", isClicked: false },
        { name: "로드샵", isClicked: false },
        { name: "디자이너브랜드", isClicked: false },
        { name: "제너럴 브랜드", isClicked: false },
        { name: "내셔럴 브랜드", isClicked: false },
        { name: "뷰티", isClicked: false },
      ],
    };
  },
  methods: {
    clickBtn(data) {
      if (data.index === 0) {
        this.mdList[data.index].isClicked = true;
        for (let i = 1; i < this.mdList.length; i++) {
          this.mdList[i].isClicked = false;
        }
      } else {
        this.mdList[data.index].isClicked = !this.mdList[data.index].isClicked;

        if (this.clearBtn()) {
          this.mdList[0].isClicked = true;
          for (let i = 1; i < this.mdList.length; i++) {
            this.mdList[i].isClicked = false;
          }
        }
        if (!this.clearBtn()) {
          this.mdList[0].isClicked = true;
        }
        for (let i = 1; i < this.mdList.length; i++) {
          if (this.mdList[i].isClicked) {
            this.mdList[0].isClicked = false;
          }
        }
      }
    },
    clearBtn() {
      let result = true;
      for (let i = 1; i < this.mdList.length; i++) {
        if (!this.mdList[i].isClicked) {
          return (result = false);
        }
      }
      return result;
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
