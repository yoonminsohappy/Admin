<template>
  <div class="opion-frame">
    <div class="opion-floater" v-bind:class="{ super_top: opion_list_open }">
      <div class="close-button-container">
        <div class="list-content-card" v-on:click="opion_list_opener">{{ selected_name }}</div>
      </div>
      <div v-if="opion_list_open">
        <div class="opion-input">
          <input type="text" />
        </div>
        <div class="list-content-list">
          <div
            class="list-content-card hover"
            v-for="list in props_list"
            v-bind:key="list.id"
            v-on:click="select_contents(list)"
          >{{ list.name }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "opion-list",
  components: {},
  props: ["props_list", "idx_num", "selected_name"],
  data: () => ({
    test: "",
    opion_list_open: false,
    selected_id: "",
    datas: { now_option_list: [] },
  }),
  computed: {},
  methods: {
    opion_list_opener: function () {
      this.opion_list_open = !this.opion_list_open;
    },
    select_contents: function (obj) {
      this.selected_id = obj.id;
      this.$emit("selected_content", {
        id: obj.id,
        name: obj.name,
        idx: this.idx_num,
      });
      this.opion_list_open = false;
    },
  },
};
</script>

<style lang="scss">
.opion-frame {
  position: relative;
  width: 100%;

  .opion-floater {
    position: absolute;
    display: flex;
    flex-direction: column;
    justify-content: center;
    width: 100%;
    border: 1px solid #dddddd;
    border-radius: 5px;
    padding-left: 5px;
    padding-right: 5px;
    background-color: #ffffff;
  }

  .super_top {
    z-index: 999999;
  }

  .close-button-container {
    display: flex;
    justify-content: space-between;
    align-items: center;

    .close-button {
      color: #8e8e8e;
      padding: 3px;
      cursor: pointer;
    }
  }

  .opion-input {
    font-size: 14px;
    border: 1px solid #dddddd;
    margin-top: 5px;
    margin-bottom: 5px;
    padding: 6px;

    input {
      width: 100%;
    }
  }

  .list-content-card {
    display: flex;
    align-items: center;
    width: 100%;
    height: 37px;
    font-size: 14px;
    padding: 3px 7px 4px;
    cursor: pointer;
  }

  .hover:hover {
    background-color: #eeeeee;
  }
}
</style>
