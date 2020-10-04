<template>
  <div>
    <div class="spiner"></div>
    <div class="comment-box">
      <span>데이터를 불러오고 있습니다.</span>
    </div>
  </div>
</template>

<script>
export default {};
</script>

<style scoped lang="scss">
.spiner {
  z-index: 50;
  border: none;
  margin: 0px;
  padding: 0px;
  width: 100%;
  height: 100%;
  position: absolute;
  top: 0px;
  left: 0px;
  background-color: rgb(0, 0, 0);
  cursor: wait;
  opacity: 0.6;
}
.comment-box {
  z-index: 60;
  position: absolute;
  padding: 0px;
  margin: 0px;
  width: 20%;
  top: 55%;
  left: 42%;
  text-align: center;
  color: rgb(0, 0, 0);
  border: 1px solid rgb(170, 170, 170);
  background-color: rgb(255, 255, 255);
  cursor: wait;

  span {
    cursor: wait;
    text-align: center;
    color: rgb(0, 0, 0);
  }
}
</style>
