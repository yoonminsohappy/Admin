<template>
  <div class="sign-up">
    <img
      alt="logo"
      src="https://sadmin.brandi.co.kr/include/img/logo_seller_admin_1.png"
      class="logo-img"
    />
    <div class="sign-up-container">
      <div class="seller-sign-up">셀러회원 가입</div>
      <div class="sign-up-info-box">
        <div class="sign-up-info-text">가입 정보</div>
        <div class="sign-up-id-wrapper">
          <input
            class="sign-up-id"
            type="text"
            placeholder="아이디"
            v-model="seller_account"
            @input="isShownId"
          />
          <div class="warning-message" v-show="showId">
            {{ warningIdText }}
          </div>
        </div>
        <div class="sign-up-pwd-wrapper">
          <input
            class="sign-up-pwd"
            type="password"
            placeholder="비밀번호"
            v-model="password"
            @input="isPwd"
          />
          <div class="warning-message" v-show="showPwd">
            {{ warningPwd }}
          </div>
        </div>
        <div class="check-pwd-wrapper">
          <input
            class="check-pwd"
            type="password"
            placeholder="비밀번호 재입력"
            v-model="checkingPwd"
            @input="checkPwd"
          />
          <div class="warning-message" v-show="showcheckingPwd">
            {{ this.warnCheckingPwd }}
          </div>
        </div>
      </div>
      <div class="manager-info-box">
        <div class="manager-info-text">담당자 정보</div>
        <input
          class="manager-phone-num"
          type="text"
          placeholder="핸드폰번호"
          v-model="phone_number"
          @input="isManagerPhoneNumber"
        />
        <div class="warning-message" v-show="showManagerPhoneNum">
          {{ warningManagerPhoneNumber }}
        </div>
      </div>
      <div class="seller-info-box">
        <div class="seller-info-text">셀러 정보</div>
        <div class="radio-list">
          <span
            class="each-radio"
            v-for="(item, index) in eachRadioBtn"
            v-bind:key="index"
          >
            <input
              class="seller-option"
              type="radio"
              :checked="index === 0 ? true : false"
              name="radio-btn"
              @click="isActive(index)"
            />{{ item.name }}
          </span>
        </div>
        <div class="seller-info-list">
          <div class="seller-name-box">
            <input
              class="each-seller-info"
              type="text"
              placeholder="셀러명 (상호)"
              v-model="korean_name"
              @input="isSellerName"
            />
            <div class="warning-message" v-show="showSellerName">
              필수 입력 항목입니다.
            </div>
          </div>
          <div class="seller-name-eng-box">
            <input
              class="each-seller-eng-info"
              type="text"
              placeholder="영문 셀러명 (영문상호)"
              v-model="english_name"
              @input="isSellerEng"
            />
            <div class="warning-message" v-show="showSellerEng">
              {{ warningSellerEng }}
            </div>
          </div>
          <div class="seller-num-box">
            <input
              class="each-seller-info"
              type="text"
              placeholder="고객센터 전화번호"
              v-model="cs_phone"
              @input="isServiceCenterNum"
            />
          </div>
          <div class="warning-message" v-show="showServiceCenterNum">
            {{ warningServiceCenterNum }}
          </div>
        </div>
      </div>
      <div class="btn-wrapper">
        <button class="submit-btn" @click="handleSubmitBtn">신청</button>
        <button class="cancel-btn">취소</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { config } from "../../api/index";

export default {
  data: () => ({
    isActiveBtn: 0,
    eachRadioBtn: [
      {
        id: 1,
        name: "쇼핑몰",
      },
      {
        id: 2,
        name: "마켓",
      },
      {
        id: 3,
        name: "로드샵",
      },
      {
        id: 4,
        name: "디자이너브랜드",
      },
      {
        id: 5,
        name: "제너럴브랜드",
      },
      {
        id: 6,
        name: "내셔널브랜드",
      },
      {
        id: 7,
        name: "뷰티",
      },
    ],
    seller_account: "",
    password: "",
    checkingPwd: "",
    cs_phone: "",
    english_name: "",
    korean_name: "",
    phone_number: "",
    seller_properties: "쇼핑몰",
    showId: false,
    warningIdText:
      " 아이디는 5~20글자의 영문, 숫자, 언더바, 하이픈만 사용 가능하며 시작문자는 영문 또는 숫자입니다.",
    warningServiceCenterNum:
      "고객센터 전화번호는 숫자와 하이픈만 입력가능합니다.",
    showServiceCenterNum: false,
    warningSellerEng: "셀러 영문명은 소문자만 입력가능합니다.",
    showSellerEng: false,
    showSellerName: false,
    showManagerPhoneNum: false,
    warningManagerPhoneNumber: "필수 입력항목입니다.",
    showPwd: false,
    warningPwd:
      " 비밀번호는 8~20글자의 영문대소문자, 숫자, 특수문자를 조합해야합니다.",
    warnCheckingPwd: "비밀번호가 일치하지 않습니다.",
    showcheckingPwd: false,
  }),
  methods: {
    isShownId() {
      if (
        this.seller_account.match(
          /^(?=.*[a-zA-Z])(?=.*[_-])(?=.*[0-9]).{5,20}$/
        )
      ) {
        this.showId = false;
      }
      if (
        !this.seller_account.match(
          /^(?=.*[a-zA-Z])(?=.*[_-])(?=.*[0-9]).{5,20}$/
        )
      ) {
        this.showId = true;
        this.warningIdText =
          " 아이디는 5~20글자의 영문, 숫자, 언더바, 하이픈만 사용 가능하며 시작문자는 영문 또는 숫자입니다.";
      }
      if (this.seller_account.length < 5) {
        this.showId = true;
        this.warningIdText = "아이디의 최소 길이는 5글자입니다.";
      }

      if (this.seller_account.length < 1) {
        this.showId = true;
        this.warningIdText = "필수 입력항목입니다.";
      }
    },
    isServiceCenterNum() {
      if (this.cs_phone.match(/^[0-9]{2,3}[-]+[0-9]{3,4}[-]+[0-9]{3,4}$/)) {
        this.showServiceCenterNum = false;
      }
      if (!this.cs_phone.match(/^[0-9]{2,3}[-]+[0-9]{3,4}[-]+[0-9]{3,4}$/)) {
        this.showServiceCenterNum = true;
      }
      if (this.cs_phone.length < 1) {
        this.warningServiceCenterNum = "필수 입력항목입니다.";
      }
    },
    isSellerEng() {
      if (this.english_name.match(/^[a-z]+$/)) {
        this.showSellerEng = false;
      }
      if (!this.english_name.match(/^[a-z]+$/)) {
        this.showSellerEng = true;
        this.warningSellerEng = "셀러 영문명은 소문자만 입력가능합니다.";
      }
      if (this.english_name.length < 1) {
        this.showSellerEng = true;
        this.warningSellerEng = "필수 입력항목입니다.";
      }
    },
    isSellerName() {
      if (this.korean_name.length < 1) {
        this.showSellerName = true;
      } else {
        this.showSellerName = false;
      }
    },
    isManagerPhoneNumber() {
      if (this.phone_number.match(/^\d{3}-\d{3,4}-\d{4}$/)) {
        this.showManagerPhoneNum = false;
      }
      if (!this.phone_number.match(/^\d{3}-\d{3,4}-\d{4}$/)) {
        this.showManagerPhoneNum = true;
        this.warningManagerPhoneNumber = "올바른 정보를 입력해주세요.";
      }
      if (this.phone_number.length < 1) {
        this.showManagerPhoneNum = true;
        this.warningManagerPhoneNumber = "필수 입력항목입니다.";
      }
    },
    isPwd() {
      if (
        this.password.match(
          /^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,20}$/
        )
      ) {
        this.showPwd = false;
      }
      if (
        !this.password.match(
          /^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,20}$/
        )
      ) {
        this.showPwd = true;
        this.warningPwd =
          "비밀번호는 8~20글자의 영문대소문자, 숫자, 특수문자를 조합해야합니다.";
      }
      if (this.password.length < 1) {
        this.showPwd = true;
        this.warningPwd = "필수 입력항목입니다.";
      }
    },
    checkPwd() {
      if (this.password === this.checkingPwd) {
        this.showcheckingPwd = false;
      }
      if (this.password !== this.checkingPwd) {
        this.showcheckingPwd = true;
      }
    },
    isActive(index) {
      this.isActiveBtn = index;
      this.seller_properties = this.eachRadioBtn[index].name;
    },
    showSellerProperties() {
      this.seller_properties = "";
    },
    handleSubmitBtn() {
      axios
        .post(`${config}sellers/signup`, {
          seller_account: this.seller_account,
          password: this.password,
          seller_property: this.seller_properties,
          phone_number: this.phone_number,
          korean_name: this.korean_name,
          english_name: this.english_name,
          cs_phone: this.cs_phone,
        })
        .then((response) => {
          // 회원가입 후 로그인 창으로 이동
          this.$router.push("/");
          console.log("signup>>>>>>>SUCCESS");
        });
    },
  },
};
</script>

<style lang="scss">
.sign-up {
  background-color: #fafafa;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  height: 100%;

  .logo-img {
    width: 180px;
    height: 90px;
    padding-bottom: 15px;
    margin-top: 60px;
  }

  .sign-up-container {
    width: 600px;
    height: 1150px;
    background-color: white;
    padding: 60px;
    display: flex;
    flex-direction: column;
    align-items: center;

    .seller-sign-up {
      font-size: 30px;
      font-weight: 300;
      border-bottom: 1px solid #e0dfdf;
      padding-bottom: 20px;
      text-align: center;
      width: 470px;
    }

    .sign-up-info-box {
      display: flex;
      flex-direction: column;

      .sign-up-info-text {
        font-weight: 300;
        font-size: 24px;
        margin-top: 70px;
      }

      .sign-up-id-wrapper {
        position: relative;
        &::before {
          font-family: FontAwesome;
          content: "\f007";
          position: absolute;
          left: 13px;
          top: 30px;
        }
        .sign-up-id {
          width: 440px;
          height: 45px;
          border: 1px solid #e5e5e5;
          border-radius: 4px;
          padding-left: 33px;
          margin-top: 15px;
          &:focus {
            outline: 1px solid #333333;
          }
        }
        .warning-message {
          margin-top: 10px;
          color: #a94442;
        }
      }

      .sign-up-pwd-wrapper {
        position: relative;
        &::before {
          font-family: FontAwesome;
          content: "\f023";
          position: absolute;
          left: 13px;
          top: 30px;
        }
        .sign-up-pwd {
          width: 440px;
          height: 45px;
          border: 1px solid #e5e5e5;
          border-radius: 4px;
          padding-left: 33px;
          margin-top: 15px;
          &:focus {
            outline: 1px solid #333333;
          }
        }
        .warning-message {
          margin-top: 10px;
          color: #a94442;
        }
      }

      .check-pwd-wrapper {
        position: relative;
        &::before {
          font-family: FontAwesome;
          content: "\f00c";
          position: absolute;
          left: 13px;
          top: 30px;
        }
        .check-pwd {
          width: 440px;
          height: 45px;
          border: 1px solid #e5e5e5;
          border-radius: 4px;
          padding-left: 33px;
          margin-top: 15px;
          &:focus {
            outline: 1px solid #333333;
          }
        }
        .warning-message {
          margin-top: 10px;
          color: #a94442;
        }
      }
    }

    .manager-info-box {
      margin-right: 5px;
      position: relative;
      &::before {
        font-family: FontAwesome;
        content: "\f095";
        position: absolute;
        left: 13px;
        top: 92px;
      }
      .manager-info-text {
        font-weight: 300;
        font-size: 24px;
        margin-top: 35px;
      }

      .manager-phone-num {
        width: 440px;
        height: 45px;
        border: 1px solid #e5e5e5;
        border-radius: 4px;
        padding-left: 33px;
        margin-top: 15px;
        &:focus {
          outline: 1px solid #333333;
        }
      }
      .warning-message {
        margin-top: 10px;
        color: #a94442;
      }
    }

    .seller-info-box {
      margin-right: 8px;
      .seller-info-text {
        font-weight: 300;
        font-size: 24px;
        margin-top: 35px;
      }

      .radio-list {
        width: 380px;
        height: 42.5px;
        margin-top: 10px;
        margin-bottom: 10px;

        .each-radio {
          margin-right: 20px;

          .seller-option {
            margin-right: 5px;
            margin-bottom: 10px;
            border: 1px solid red;
          }
        }
      }

      .seller-info-list {
        display: flex;
        flex-direction: column;

        .seller-name-box {
          position: relative;
          &::before {
            font-family: FontAwesome;
            content: "\f031";
            position: absolute;
            left: 12px;
            top: 29px;
          }
          .each-seller-info {
            width: 440px;
            height: 45px;
            border: 1px solid #e5e5e5;
            border-radius: 4px;
            padding-left: 33px;
            margin-top: 15px;

            &:focus {
              outline: 1px solid #333333;
            }
          }

          .warning-message {
            margin-top: 10px;
            color: #a94442;
          }
        }

        .seller-name-eng-box {
          position: relative;
          &::before {
            font-family: FontAwesome;
            content: "\f031";
            position: absolute;
            left: 12px;
            top: 29px;
          }
          .each-seller-eng-info {
            width: 440px;
            height: 45px;
            border: 1px solid #e5e5e5;
            border-radius: 4px;
            padding-left: 33px;
            margin-top: 15px;

            &:focus {
              outline: 1px solid #333333;
            }
          }

          .warning-message {
            margin-top: 10px;
            color: #a94442;
          }
        }
        .seller-num-box {
          position: relative;
          &::before {
            font-family: FontAwesome;
            content: "\f095";
            position: absolute;
            left: 13px;
            top: 29px;
          }
          .each-seller-info {
            width: 440px;
            height: 45px;
            border: 1px solid #e5e5e5;
            border-radius: 4px;
            padding-left: 33px;
            margin-top: 15px;
            &:focus {
              outline: 1px solid #333333;
            }
          }
        }
        .warning-message {
          margin-top: 10px;
          color: #a94442;
        }
      }
    }

    .btn-wrapper {
      width: 120px;
      display: flex;
      margin-top: 55px;

      .submit-btn {
        color: #fff;
        background-color: #5bc0de;
        border-color: #46b8da;
        width: 70px;
        height: 44px;
        border-top-left-radius: 4px;
        border-bottom-left-radius: 4px;
        outline: none;
      }

      .cancel-btn {
        color: #fff;
        background-color: #d9534f;
        border-color: #d43f3a;
        width: 70px;
        height: 44px;
        border-top-right-radius: 4px;
        border-bottom-right-radius: 4px;
        outline: none;
      }
    }
  }
}
</style>
