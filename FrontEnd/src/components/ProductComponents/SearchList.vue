<template>
  <div class="search-frame">
    <div class="search-floater">
      <div class="close-button-container">
        <div
          v-bind:class="{
            'list-content-name': !selected_photo,
            'list-content-card': selected_photo,
          }"
          v-on:click="search_list_opener"
        >
          <img
            alt="list-content profile"
            v-bind:src="selected_photo"
            v-if="selected_photo"
          />
          {{ selected_name }}
        </div>
        <span
          class="close-button"
          v-on:click="search_reseter"
          v-if="selected_name !== 'Select...'"
          >x</span
        >
      </div>
      <div v-if="search_list_open">
        <div class="search-input">
          <input type="text" v-on:change="search_text_inputer" />
        </div>
        <div class="list-content-list">
          <div
            class="list-content-card hover"
            v-for="list in datas"
            v-bind:key="list.content_name"
            v-on:click="select_contents(list)"
          >
            <img
              alt="list-content profile"
              v-bind:src="list.profile_image"
              v-if="list.profile_image"
            />
            {{ list.korean_name }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { config } from "../../api/index";

export default {
  name: "search-list",
  components: {},
  props: [],
  data: () => ({
    search_list_open: false,
    selected_photo: "",
    selected_id: "",
    selected_name: "Select...",
    datas: {},
  }),
  computed: {},
  methods: {
    search_list_opener: function () {
      this.search_list_open = !this.search_list_open;
    },
    select_contents: function (obj) {
      this.selected_photo = obj.profile_image;
      this.selected_id = obj.seller_property_id;
      this.selected_name = obj.korean_name;
      this.$emit("selected_id", obj.seller_property_id);
      this.$emit("selected_name", obj.korean_name);
      this.search_list_open = false;
    },
    search_text_inputer: function (e) {
      let query = e.target.value;

      axios
        .get(`${config}products/sellers?q=${query}`, {
          headers: {
            Authorization: localStorage.getItem("access_token"),
          },
        })
        .then((res) => (this.datas = res.data));

      // axios
      //   .get(`public/mockdata/${query}.json`)
      //   .then((res) => (this.datas = res.data));
    },
    search_reseter: function () {
      this.selected_photo = "";
      this.selected_id = "";
      this.selected_name = "Select...";
    },
  },
};
</script>

<style lang="scss">
.search-frame {
  position: relative;

  .search-floater {
    position: absolute;
    display: flex;
    flex-direction: column;
    justify-content: center;
    width: 282px;
    border: 1px solid #dddddd;
    border-radius: 5px;
    padding-left: 5px;
    padding-right: 5px;
    background-color: #ffffff;
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

  .hover:hover {
    background-color: #eeeeee;
  }

  .list-content-name {
    display: flex;
    align-items: center;
    width: 100%;
    height: 34px;
    font-size: 14px;
    color: #999999;
    padding-left: 10px;
    cursor: pointer;
  }

  .search-input {
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

    img {
      width: 30px;
      height: 30px;
      margin-right: 10px;
    }
  }
}
</style>
