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
        <div class="id-text">intern_master</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {};
</script>

<style lang="scss">
.nav {
  position: fixed;
  top: 0;
  .nav-container {
    background-color: #873b53;
    height: 45px;
    width: 1440px;
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
      .id-text {
        height: 45px;
        color: #cecfd3;
        border-left: 1px solid black;
        padding-top: 13px;
        padding-left: 10px;
        &::after {
          font-family: FontAwesome;
          content: "\f107";
          position: absolute;
          margin-left: 10px;
        }
      }
    }
  }
}
</style>
