<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
  export default {
    name: 'App',
  }
</script>

<style lang="scss">
  *,
  *::before,
  *::after {
    box-sizing: border-box;
  }

  body {
    background-color: #f6f6f6;
  }

  a {
    color: #58e;
  }

  .van-uploader__upload {
    margin-right: 0 !important;
  }

  .van-uploader__preview:nth-child(4n) {
    margin-right: 0 !important;
  }
</style>
