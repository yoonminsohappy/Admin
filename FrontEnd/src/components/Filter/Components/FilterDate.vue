<template>
  <div class="filter-date">
    <div class="date-title">
      <label class="date-text">주문완료일 : </label>
    </div>
    <div class="select-date">
      <input
        type="button"
        class="date-btn"
        :class="{ 'clicked-btn': item.isClicked }"
        v-for="(item, index) in dateBtn"
        :key="index"
        :value="item.name"
        @click="btnClick({ item, index })"
      />
    </div>
    <div class="date-picker">
      <date-picker
        v-model="from"
        format="yyyy-MM-dd"
        type="text"
        placeholder="클릭해주세요."
      ></date-picker>
      <span class="during-text"> ~ </span>
      <date-picker
        v-model="to"
        format="yyyy-MM-dd"
        type="text"
        placeholder="클릭해주세요."
      ></date-picker>
    </div>
  </div>
</template>

<script>
import DatePicker from "vuejs-datepicker";
import { mapGetters, mapActions } from "vuex";

export default {
  data() {
    return {
      dateBtn: [
        { name: "전체", isClicked: false },
        { name: "오늘", isClicked: false },
        { name: "3일", isClicked: true },
        { name: "1주일", isClicked: false },
        { name: "1개월", isClicked: false },
        { name: "3개월", isClicked: false },
      ],
    };
  },
  computed: {
    ...mapGetters("order", ["fromData", "toData"]),
    from: {
      get() {
        return this.fromData;
      },
      set(value) {
        this.setFromDate(value);
      },
    },
    to: {
      get() {
        return this.toData;
      },
      set(value) {
        this.setToDate(value);
      },
    },
  },
  methods: {
    ...mapActions("order", ["setFromDate", "setToDate"]),
    btnClick(data) {
      this.dateBtn[data.index].isClicked = true;
      this.clearClicked(data.index);
      this.$store.commit("order/setDate", data);
    },
    clearClicked(idx) {
      for (let i = 0; i < this.dateBtn.length; i++) {
        if (i !== idx) {
          this.dateBtn[i].isClicked = false;
        }
      }
    },
  },
  components: {
    DatePicker,
  },
};
</script>

<style lang="scss">
.filter-date {
  display: flex;
  margin-bottom: 10px;
  padding: 0 15px;
  font-size: 13px;

  .date-title {
    width: 125px;

    .date-text {
      padding-top: 7px;
      height: 30px;
      font-weight: 400;
      font-size: 14px;
      min-width: 70px;
      margin-bottom: 5px;
    }
  }

  .select-date {
    .date-btn {
      margin-right: 3px;
      cursor: pointer;
      border-color: #e5e5e5;
      border: 1px solid transparent;
      border-radius: 4px;
      color: #333;
      background-color: #fff;
      padding: 6px 12px;
      font-size: 14px;
      border-color: #e5e5e5;

      &:hover {
        color: #333;
        background-color: #e6e6e6;
        border-color: #adadad;
      }

      &:focus {
        outline: none;
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

  .date-picker {
    display: flex;
    cursor: pointer;

    input[type="text"] {
      border-radius: 3px 0 0 3px;
      text-align: center;
      color: #333333;
      background-color: white;
      border: 1px solid #e5e5e5;
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
      height: 34px;
      padding: 10px 12px;
      text-align: center;
    }
  }
}
@media (max-width: 1080px) {
  .filter-date {
    display: block;
  }
}
</style>
