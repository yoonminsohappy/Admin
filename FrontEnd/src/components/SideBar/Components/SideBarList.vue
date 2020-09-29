<template>
  <div>
    <div
      class="menu-list"
      v-bind:class="{ 'menu-list-clicked': openState }"
      v-on:click="openMenuItem"
    >
      <font-awesome-icon class="icon" v-bind:icon="sideMenuList.icon" />
      <span class="title">{{ sideMenuList.name }}</span>
      <font-awesome-icon
        class="arrow"
        v-bind:class="{ 'arrow-clicked': openState }"
        icon="angle-left"
      />
    </div>
    <ul class="open-menu" v-bind:class="{ 'open-menu-clicked': openState }">
      <div
        v-for="(openMenu, index) in sideMenuList.openMenuList"
        v-bind:key="index"
      >
        <open-menu v-bind:openMenuList="openMenu"></open-menu>
      </div>
    </ul>
  </div>
</template>

<script>
import OpenMenu from "./OpenMenu";

export default {
  props: ["sideMenuList"],
  data: function () {
    return { openState: false };
  },
  methods: {
    openMenuItem: function () {
      this.openState = !this.openState;
    },
  },
  components: { OpenMenu },
};
</script>

<style lang="scss" scoped>
.menu-list {
  position: relative;
  border-bottom: 1px solid #414247;
  border-right: 4px solid transparent;
  padding: 10px 13px 10px 15px;
  font-size: 14px;
  font-weight: 300;
  display: flex;
  align-items: center;

  &:hover {
    background: #2b2b30;
  }
  .icon {
    color: #999;
    font-size: 16px;
    margin-right: 10px;
    width: 1.25em;
  }
  .title {
    color: #eee;
    font-size: 14px;
    font-weight: 300;
  }
  .arrow {
    position: absolute;
    right: 18px;
    color: #414247;
    font-size: 16px;
    margin-right: 5px;
  }
  .arrow-clicked {
    color: #ffffff;
    transform: rotate(-90deg);
  }
}
.open-menu {
  display: none;
  margin: 8px 0;
  font-size: 14px;
  font-weight: 300;
  animation: rotateMenu 300ms ease-in-out forwards;
  transform-origin: top center;
  @keyframes rotateMenu {
    0% {
      transform: rotateX(-90deg);
    }
    100% {
      transform: rotateX(0deg);
    }
  }
}
.open-menu-clicked {
  display: block;
}
.menu-list-clicked {
  background: #2b2b30;
  border-right: 4px solid red;
  border-bottom: none;
}
</style>
