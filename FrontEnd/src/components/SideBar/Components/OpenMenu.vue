<template>
  <li class="menu-items">
    <router-link :to="openMenuList.url" class="menu-item">
      {{ openMenuList.name }}
    </router-link>
  </li>
</template>

<script>
export default {
  props: ["openMenuList"],
};
</script>

<style lang="scss" scoped>
.menu-items {
  margin-top: 1px;

  .menu-item {
    display: block;
    color: #cecfd3;
    text-decoration: none;
    padding: 5px 0 5px 35px;

    &:hover {
      background: #414247;
      color: #ffffff;
    }
  }
}
</style>
