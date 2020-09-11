<!-- home -->
<template>
  <div class="index-container">
    <div class="warpper">
      <h1 class="demo-home__title"><img src="https://imgs.solui.cn/weapp/logo.png"/><span> 宠物识别</span></h1>
      <h2 class="demo-home__desc">
        使用到的AWS技术
      </h2>
    </div>
    <van-cell icon="success" v-for="item in list" :key="item" :title="item"/>
  </div>
</template>

<script>
export default {
  data() {
    return {
      list: [
        'Amazon S3',
        'Amazon SageMaker',
        'aws-sdk-js',
      ]
    }
  },

  computed: {},

  mounted() {
  },

  methods: {}
}
</script>
<style lang="scss" scoped>
.index-container {
  .warpper {
    padding: 12px;
    background: #fff;

    .demo-home__title {
      margin: 0 0 6px;
      font-size: 32px;

      .demo-home__title img,
      .demo-home__title span {
        display: inline-block;
        vertical-align: middle;
      }

      img {
        width: 32px;
      }

      span {
        margin-left: 16px;
        font-weight: 500;
      }
    }

    .demo-home__desc {
      margin: 0 0 20px;
      color: rgba(69, 90, 100, 0.6);
      font-size: 14px;
    }
  }
}
</style>
