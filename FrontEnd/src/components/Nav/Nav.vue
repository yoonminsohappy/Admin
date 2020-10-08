<template>
  <div class="nav">
    <div class="nav-container">
      <div class="left-container">
        <div class="img-container">
          <img
            class="logo-image"
            src="https://sadmin.brandi.co.kr/include/img/logo_2.png"
          />
          <div class="icon"></div>
        </div>
        <div class="staging-text">staging (staging)</div>
      </div>
      <div class="right-container">
        <button class="id-wrapper">
          <div class="id-text">{{ this.sellerId }}</div>
        </button>
        <div class="dropdown-content">
          <a @click="logout">Log Out</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data: function() {
    return {
      sellerId: "",
    };
  },
  methods: {
    logout() {
      this.$router.push("/");
      localStorage.removeItem("id");
    },
  },
  created() {
    this.sellerId = localStorage.getItem("id");
  },
};
</script>

<style lang="scss" scoped>
.nav {
  position: fixed;
  width: 100vw;
  top: 0;
  z-index: 999999999999999999999999;
  .nav-container {
    background-color: #873b53;
    height: 45px;
    width: 100%;
    top: -45px;
    left: -215px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-right: 40px;
    padding-left: 8px;

    .left-container {
      display: flex;
      align-items: center;
      justify-content: space-around;
      width: 280px;
      .img-container {
        .logo-image {
          width: 100px;
          height: 21.47px;
          color: white;
        }
        .icon {
          color: #cecfd3;
          &::after {
            font-family: FontAwesome;
            content: "\f107";
            position: absolute;
            left: 135px;
            top: 12px;
          }
        }
      }
      .staging-text {
        color: white;
      }
    }

    .right-container {
      position: relative;
      display: inline-block;
      &:hover .dropdown-content {
        display: block;
        cursor: pointer;
      }
      .id-wrapper {
        width: 150px;
        height: 45px;
        &:hover {
          background-color: #414247;
        }
        .id-text {
          height: 45px;
          color: #cecfd3;
          border-left: 1px solid black;
          padding-top: 13px;
          &::after {
            font-family: FontAwesome;
            content: "\f107";
            position: absolute;
            margin-left: 10px;
          }
        }
      }
      .dropdown-content {
        display: none;
        position: absolute;
        background-color: #f1f1f1;
        min-width: 160px;
        box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
        z-index: 1;
        a {
          color: black;
          padding: 18px 16px 12px 35px;
          text-decoration: none;
          display: block;

          &:hover {
            background-color: #ddd;
          }
          &::before {
            font-family: FontAwesome;
            content: "\f084";
            position: absolute;
            left: 10px;
            top: 18px;
          }
        }
      }
    }
  }
}
</style>
