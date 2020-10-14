<template>
  <div class="account">
    <span class="title">셀러 계정 관리</span>
    <span class="sub-title">셀러 회원 목록 / 관리</span>
    <div class="sub-nav">회원관리 > 셀러 계정 관리 > 셀러 회원 리스트</div>
    <div class="seller-list-container">
      <div class="seller-list-nav">셀러 회원 리스트</div>
      <div class="pagination-panel-wrapper">
        <span class="pagination-panel">Page</span>
        <button class="left-button" @click="goPrev"><</button>
        <input class="pagination-info" type="text" v-model="this.page" />
        <button class="right-button" @click="goNext">></button>
        <span>of</span>
        <span>{{ this.total_page }}</span>
        <span>| View</span>
        <select class="records-list" @change="getPerPage($event)">
          <option value="10">10</option>
          <option value="20">20</option>
          <option value="50">50</option>
          <option value="100">100</option>
          <option value="150">150</option>
        </select>
        <span>records</span>
        <span>|</span>
        <span>Found total</span>
        <span>{{ this.total_count }}</span>
        <span>records</span>
      </div>
      <div class="table-container">
        <thead>
          <tr>
            <th></th>
            <th>번호</th>
            <th>셀러아이디</th>
            <th>영문이름</th>
            <th>한글이름</th>
            <th>담당자이름</th>
            <th>셀러상태</th>
            <th>담당자 연락처</th>
            <th>담당자이메일</th>
            <th>셀러속성</th>
            <th>상품개수</th>
            <th>등록일시</th>
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
            <td>
              <select>
                <option>Select</option>
                <option>입점대기</option>
                <option>입점</option>
                <option>퇴점</option>
                <option>퇴점대기</option>
                <option>휴점</option>
              </select>
            </td>
            <td>
              <input type="text" />
            </td>
            <td>
              <input type="text" />
            </td>
            <td>
              <select>
                <option>Select</option>
                <option>쇼핑몰</option>
                <option>마켓</option>
                <option>로드샵</option>
                <option>디자이너브랜드</option>
                <option>제너럴브랜드</option>
                <option>내셔널브랜드</option>
                <option>뷰티</option>
              </select>
            </td>
            <td>
              <input />
            </td>
            <td>
              <input />
            </td>
          </tr>
          <tr v-for="(items, index) in fetchedData" v-bind:key="index">
            <td>
              <input type="checkbox" />
            </td>
            <td>{{ items.id }}</td>
            <td>{{ items.seller_account }}</td>
            <td>{{ items.english_name }}</td>
            <td>{{ items.korean_name }}</td>
            <td>{{ items.manager_name }}</td>
            <td>{{ items.seller_status }}</td>
            <td>{{ items.manager_phone_number }}</td>
            <td>{{ items.manager_email }}</td>
            <td>{{ items.seller_property }}</td>
            <td>{{ items.registered_product_count }}</td>
            <td>{{ items.register_date }}</td>
          </tr>
        </tbody>
      </div>
      <div class="pagination-panel-wrapper">
        <span class="pagination-panel">Page</span>
        <button class="left-button" @click="goPrev"><</button>
        <input class="pagination-info" type="text" v-model="this.page" />
        <button class="right-button" @click="goNext">></button>
        <span>of</span>
        <span>{{ this.total_page }}</span>
        <span>| View</span>
        <select class="records-list" @change="getPerPage($event)">
          <option value="10">10</option>
          <option value="20">20</option>
          <option value="50">50</option>
          <option value="100">100</option>
          <option value="150">150</option>
        </select>
        <span>records</span>
        <span>|</span>
        <span>Found total</span>
        <span>{{ this.total_count }}</span>
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
      .get(`${config}sellers?page=${this.page}&per_page=${this.per_page}`, {
        headers: {
          Authorization: localStorage.getItem("access_token"),
        },
      })
      .then((response) => {
        this.fetchedData = response.data.seller_list;
        this.total_page = response.data.total_page;
        this.total_count = response.data.total_count;
      })
      .catch((error) => console.log(error));
  },
  methods: {
    goNext() {
      if (this.total_page <= this.page) {
        axios
          .get(`${config}sellers?page=${this.page}&per_page=${this.per_page}`, {
            headers: {
              Authorization: localStorage.getItem("access_token"),
            },
          })
          .then((response) => {
            this.fetchedData = response.data.seller_list;
          });
        return;
      } else {
        this.page = this.page + 1;
        axios
          .get(`${config}sellers?page=${this.page}&per_page=${this.per_page}`, {
            headers: {
              Authorization: localStorage.getItem("access_token"),
            },
          })
          .then((response) => {
            this.fetchedData = response.data.seller_list;
          });
      }
    },
    goPrev() {
      if (this.page === 1) {
        axios
          .get(`${config}sellers?page=${this.page}&per_page=${this.per_page}`, {
            headers: {
              Authorization: localStorage.getItem("access_token"),
            },
          })
          .then((response) => {
            this.fetchedData = response.data.seller_list;
          });
        return;
      } else {
        this.page = this.page - 1;
        axios
          .get(`${config}sellers?page=${this.page}&per_page=${this.per_page}`, {
            headers: {
              Authorization: localStorage.getItem("access_token"),
            },
          })
          .then((response) => {
            this.fetchedData = response.data.seller_list;
          });
      }
    },
    getPerPage(e) {
      this.per_page = e.target.value;
      axios
        .get(`${config}sellers?page=${this.page}&per_page=${this.per_page}`, {
          headers: {
            Authorization: localStorage.getItem("access_token"),
          },
        })
        .then((response) => {
          this.fetchedData = response.data.seller_list;
          this.total_page = response.data.total_page;
          this.total_count = response.data.total_count;
        });
    },
  },
};
</script>

<style lang="scss" scoped>
.account {
  .title {
    font-size: 26px;
    color: #666;
    font-weight: 330;
    margin-top: 15px;
  }
  .sub-title {
    font-size: 14px;
    color: #666;
    font-weight: 330;
  }
  .sub-nav {
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
      content: "\f015";
      position: absolute;
      left: 12px;
      top: 10px;
    }
  }
  .seller-list-container {
    overflow-x: auto;
    overflow-y: hidden;
    border: 1px solid #dddddd;

    .seller-list-nav {
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
    .pagination-panel-wrapper {
      display: flex;
      justify-content: space-between;
      align-items: center;
      width: 600px;
      height: 30;
      padding: 15px;
      .pagination-panel {
        font-size: 15px;
      }
      .left-button {
        width: 27px;
        height: 30px;
        border: 1px solid #ccc;
        border-radius: 4px;
      }
      .pagination-info {
        width: 45px;
        height: 30px;
        border: 1px solid #ccc;
        border-radius: 4px;
        text-align: center;
      }
      .right-button {
        width: 27px;
        height: 30px;
        border: 1px solid #ccc;
        border-radius: 4px;
      }
      .records-list {
        width: 80px;
        height: 30px;
        border: 1px solid #e5e5e5;
        border-radius: 4px;
      }
    }
    .table-container {
      width: 1200px;
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
