<template>
  <div class="login">
    <div class="logo-container">
      <img
        alt="logo"
        src="https://sadmin.brandi.co.kr/include/img/logo_seller_admin_1.png"
        class="logo-img"
      />
    </div>
    <div class="login-container">
      <div class="login-box">
        <span class="seller-login">셀러 로그인</span>
        <div class="id-container">
          <input
            class="id"
            type="text"
            placeholder="셀러 아이디"
            v-model="idValue"
            @input="handleId"
          />
          <div class="warning-id" v-show="alertId">아이디를 입력해주세요.</div>
        </div>

        <div class="pw-container">
          <input
            class="pw"
            type="password"
            placeholder="셀러 비밀번호"
            v-model="pwdValue"
            @input="handlePwd"
          />
          <div class="warning-pwd" v-show="alertPwd">
            비밀번호를 입력해주세요.
          </div>
        </div>
        <div class="btn-container">
          <button class="join-btn" @click="handleJoinBtn">셀러가입</button>
          <button class="login-btn" @click="handleLoginBtn">로그인</button>
        </div>
      </div>
    </div>
    <img
      alt="trandiBanner"
      src="https://brandiprod.s3-ap-northeast-1.amazonaws.com/common/banner/brandi_admin_banner_20200911.jpg"
      class="trandi-banner"
    />
    <div class="info-container">
      <div class="info-top-box">
        <span class="info-text">입점안내</span>
        <a class="go-to-brandi" href="http://www.brandiinc.com/brandi/"
          >보러가기</a
        >
      </div>
      <div class="service-center">고객센터</div>
      <div class="info-bottom-box">
        <div class="info-bottom-wrapper">
          <span class="bar"></span>
          <span class="info-bottom-text">대표번호 : 1566-1910</span>
        </div>
        <div class="info-bottom-wrapper">
          <span class="bar"></span>
          <span class="info-bottom-text">카카오톡 플러스친구 :</span>
          <a href="https://pf.kakao.com/_pSxoZu">@브랜디셀러</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Signup from "./Signup";
import axios from "axios";
import { config } from "../../api/index";

export default {
  data: function() {
    return { idValue: "", pwdValue: "", alertId: false, alertPwd: false };
  },
  methods: {
    handleId() {
      if (this.idValue.length < 1) {
        this.alertId = true;
      }
      if (this.idValue.length > 1) {
        this.alertId = false;
      }
    },
    handlePwd() {
      if (this.pwdValue.length < 1) {
        this.alertPwd = true;
      }
      if (this.pwdValue.length > 1) {
        this.alertPwd = false;
      }
    },
    handleJoinBtn() {
      this.$router.push("/signup");
    },
    handleLoginBtn(e) {
      e.preventDefault();
      axios
        .post(`${config}sellers/signin`, {
          seller_account: this.idValue,
          password: this.pwdValue,
        })
        .then((response) => {
          if (response.data.access_token) {
            localStorage.setItem("access_token", response.data.access_token);
            localStorage.setItem("id", this.idValue);
            this.$router.push("/order/paymentComplete");
          }
        });
    },
  },
};
</script>

<style lang="scss">
.login {
  background-color: #fafafa;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  padding-top: 60px;
  padding-bottom: 60px;
  width: 100%;
  height: 100%;
  .logo-container {
    .logo-img {
      width: 180px;
      padding-bottom: 15px;
    }
  }

  .login-container {
    .login-box {
      width: 450px;
      height: 400px;
      display: flex;
      flex-direction: column;
      justify-content: space-around;
      background-color: white;
      border-radius: 4px;

      .seller-login {
        font-size: 30px;
        font-weight: 300;
        margin-top: 20px;
        margin-left: 50px;
      }

      .id-container {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        margin: 0 auto;
        position: relative;
        &::before {
          font-family: FontAwesome;
          content: "\f007";
          position: absolute;
          left: 13px;
          top: 15px;
        }

        .id {
          width: 350px;
          height: 45px;
          border: 1px solid #e5e5e5;
          border-radius: 4px;
          padding-left: 33px;
          &:focus {
            outline: 1px solid #333333;
          }
        }

        .warning-id {
          margin-top: 10px;
          color: #a94442;
          font-weight: 400;
        }
      }

      .pw-container {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        margin: 0 auto;
        position: relative;

        &::before {
          font-family: FontAwesome;
          content: "\f023";
          position: absolute;
          left: 13px;
          top: 15px;
        }
        .pw {
          width: 350px;
          height: 45px;
          border: 1px solid #e5e5e5;
          border-radius: 4px;
          padding-left: 33px;
          &:focus {
            outline: 1px solid #333333;
          }
        }

        .warning-pwd {
          display: block;
          margin-top: 10px;
          color: #a94442;
          font-weight: 400;
        }
      }
    }

    .btn-container {
      display: flex;
      justify-content: center;
      align-items: center;
      margin-bottom: 20px;

      .join-btn {
        width: 92px;
        height: 42px;
        border: 1px solid #e5e5e5;
        border-radius: 4px;
        padding: 10px 15px;
        outline: none;
      }

      .login-btn {
        width: 80px;
        height: 42px;
        color: #fff;
        background-color: #5bc0de;
        border: 1px solid #46b8da;
        border-radius: 4px;
        margin-left: 15px;
        padding: 10px 15px;
        font-weight: bold;
        outline: none;
      }
    }
  }
}

.trandi-banner {
  width: 510px;
  padding-left: 30px;
}

.info-container {
  width: 450px;
  height: 180px;
  background-color: white;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  padding-left: 30px;
  padding-top: 25px;
  padding-bottom: 15px;

  .info-top-box {
    .info-text {
      font-size: 20px;
      font-weight: 300;
    }

    .go-to-brandi {
      font-size: 20px;
      font-weight: 300;
      margin-left: 5px;
    }
  }

  .service-center {
    font-size: 20px;
    font-weight: 300;
  }

  .info-bottom-box {
    display: flex;
    flex-direction: column;

    .info-bottom-wrapper {
      padding-bottom: 10px;

      .bar {
        border-left: 1px solid black;
      }

      .info-bottom-text {
        margin-left: 10px;
      }
    }
  }
}
</style>
