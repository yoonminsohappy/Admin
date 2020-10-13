<template>
  <div class="member">
    <span class="member-title">회원 관리_커뮤니티</span>
    <span class="member-sub-title">회원 목록</span>
    <div class="member-sub-nav">
      회원관리 > 회원 관리_커뮤니티 > 회원 리스트
    </div>
    <div class="member-list-container">
      <div class="member-list-nav">회원 리스트</div>
      <div class="mem-pagination-panel-wrapper">
        <span class="mem-pagination-panel">Page</span>
        <button class="mem-left-button" @click="goPrev"><</button>
        <input class="mem-pagination-info" type="text" v-model="this.page" />
        <button class="mem-right-button" @click="goNext">></button>
        <span>of</span>
        <span>{{ this.total_page }}</span>
        <span>| View</span>
        <select class="mem-records-list" @change="getPerPage($event)">
          <option value="10">10</option>
          <option value="20">20</option>
          <option value="50">50</option>
          <option value="100">100</option>
          <option value="150">150</option>
        </select>
        <span>records</span>
        <span>|</span>
        <span>Found total</span>
        <span> {{ total_count }}</span>
        <span>records</span>
      </div>
      <div class="mem-table-container">
        <thead>
          <tr>
            <th></th>
            <th>회원번호</th>
            <th>회원명</th>
            <th>휴대폰</th>
            <th>이메일</th>
            <th>등록일</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>
              <input type="checkbox" />
            </td>
            <td>
              <input type="text" />
            </td>
            <td>
              <input type="text" />
            </td>
            <td>
              <input type="text" />
            </td>
            <td>
              <input type="text" />
            </td>
            <td>
              <input type="text" />
            </td>
          </tr>
          <tr v-for="(items, index) in fetchedData" v-bind:key="index">
            <td>
              <input type="checkbox" />
            </td>
            <td>{{ items.id }}</td>
            <td>{{ items.account_id }}</td>
            <td>{{ items.phone_number }}</td>
            <td>{{ items.email }}</td>
            <td>{{ items.register_date }}</td>
          </tr>
        </tbody>
      </div>
      <div class="mem-pagination-panel-wrapper">
        <span class="mem-pagination-panel">Page</span>
        <button class="mem-left-button" @click="goPrev"><</button>
        <input class="mem-pagination-info" type="text" v-model="this.page" />
        <button class="mem-right-button" @click="goNext">></button>
        <span>of</span>
        <span>{{ this.total_page }}</span>
        <span>| View</span>
        <select class="mem-records-list" @change="getPerPage($event)">
          <option value="10">10</option>
          <option value="20">20</option>
          <option value="50">50</option>
          <option value="100">100</option>
          <option value="150">150</option>
        </select>
        <span>records</span>
        <span>|</span>
        <span>Found total</span>
        <span> {{ total_count }}</span>
        <span>records</span>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { config } from "../../api/index";
export default {
  data() {
    return {
      fetchedData: [],
      page: 1,
      per_page: 10,
      total_page: 0,
      total_count: 0,
    };
  },
  created() {
    axios
      .get(`${config}users?page=${this.page}&per_page=${this.per_page}`, {
        headers: {
          Authorization: localStorage.getItem("access_token"),
        },
      })
      .then((response) => {
        this.fetchedData = response.data.user_list;
        this.total_page = response.data.total_page;
        this.total_count = response.data.total_count;
      })
      .catch((error) => console.log(error));
  },
  methods: {
    goPrev() {
      if (this.page === 1) {
        axios
          .get(`${config}users?page=${this.page}&per_page=${this.per_page}`, {
            headers: {
              Authorization: localStorage.getItem("access_token"),
            },
          })
          .then((response) => {
            this.fetchedData = response.data.user_list;
          });
        return;
      } else {
        this.page = this.page - 1;
        axios
          .get(`${config}users?page=${this.page}&per_page=${this.per_page}`, {
            headers: { Authorization: localStorage.getItem("access_token") },
          })
          .then((response) => {
            this.fetchedData = response.data.user_list;
          });
      }
    },
    goNext() {
      if (this.total_page <= this.page) {
        axios
          .get(`${config}users?page=${this.page}&per_page=${this.per_page}`, {
            headers: {
              Authorization: localStorage.getItem("access_token"),
            },
          })
          .then((response) => {
            this.fetchedData = response.data.user_list;
          });
        return;
      } else {
        this.page = this.page + 1;
        axios
          .get(`${config}users?page=${this.page}&per_page=${this.per_page}`, {
            headers: {
              Authorization: localStorage.getItem("access_token"),
            },
          })
          .then((response) => {
            this.fetchedData = response.data.user_list;
          });
      }
    },
    getPerPage(e) {
      this.per_page = e.target.value;
      axios
        .get(`${config}users?page=${this.page}&per_page=${this.per_page}`, {
          headers: {
            Authorization: localStorage.getItem("access_token"),
          },
        })
        .then((response) => {
          this.fetchedData = response.data.user_list;
          this.total_page = response.data.total_page;
          this.total_count = response.data.total_count;
        });
    },
  },
};
</script>

<style lang="scss">
.member {
  .member-title {
    font-size: 26px;
    color: #666;
    font-weight: 330;
    margin-top: 15px;
  }
  .member-sub-title {
    font-size: 14px;
    color: #666;
    font-weight: 330;
  }
  .member-sub-nav {
    font-size: 13px;
    background-color: #eee;
    height: 34px;
    padding: 8px;
    padding-left: 35px;
    margin-top: 15px;
    margin-bottom: 10px;
    position: relative;
    &::before {
      font-family: FontAwesome;
      content: "\f0c0";
      position: absolute;
      left: 12px;
      top: 10px;
    }
  }
  .member-list-container {
    border: 1px solid #dddddd;
    .member-list-nav {
      position: relative;
      background-color: #eee;
      border-radius: 4px 4px 0 0;
      padding: 10px 10px 2px 40px;
      height: 38px;
      &::before {
        font-family: FontAwesome;
        content: "\f03a";
        position: absolute;
        left: 17px;
        top: 11px;
      }
    }
    .mem-pagination-panel-wrapper {
      display: flex;
      justify-content: space-between;
      align-items: center;
      width: 700px;
      height: 30;
      padding: 15px;
      .mem-pagination-panel {
        font-size: 15px;
      }
      .mem-left-button {
        width: 27px;
        height: 30px;
        border: 1px solid #ccc;
        border-radius: 4px;
      }
      .mem-pagination-info {
        width: 45px;
        height: 30px;
        border: 1px solid #ccc;
        border-radius: 4px;
        text-align: center;
      }
      .mem-right-button {
        width: 27px;
        height: 30px;
        border: 1px solid #ccc;
        border-radius: 4px;
      }
      .mem-records-list {
        width: 80px;
        height: 30px;
        border: 1px solid #e5e5e5;
        border-radius: 4px;
      }
    }
    .mem-table-container {
      overflow: auto;
      margin-left: 10px;
      margin-right: 10px;

      th,
      td {
        text-align: left;
        padding: 12px 8px 8px 8px;
        border: 1px solid #ddd;
      }
      th {
        font-weight: 600;
        color: black;
        font-size: 13px;
        background-color: #eee;
      }
    }
  }
}
</style>
