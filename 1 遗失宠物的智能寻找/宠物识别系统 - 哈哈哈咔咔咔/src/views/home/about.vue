<!-- home -->
<template>
  <div class="about-container">
    <div class="warpper">
      <div class="list">
        <div class="logo"></div>
        <div class="demo-home__title">宠物识别项目</div>
        <div class="item">项目作者: dwb</div>
        <div class="item"></div>
        <div class="item">使用到的AWS技术</div>
        <div class="item">
          {{ userName }}
          <van-button v-if="userName == ''" type="warning" size="small" @click="doDispatch">快点我~</van-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {mapGetters} from 'vuex'

export default {
  data() {
    return {
      wechat: `${this.$cdn}/wx/640.gif`
    }
  },
  computed: {
    ...mapGetters(['userName'])
  },
  methods: {
    // Action 通过 store.dispatch 方法触发
    doDispatch() {
      this.$store.dispatch('setUserName', 'Amazon S3、 Amazon SageMaker、 aws-sdk-js')
    },
  }
}
</script>
<style lang="scss">
.about-container {
  /* 你的命名空间 */
  background: #fff;
  height: 100vh;
  box-sizing: border-box;

  .warpper {
    padding: 50px 12px 12px 12px;

    .list {
      display: flex;
      flex-direction: column;
      align-items: center;
      color: #666;
      font-size: 14px;

      .demo-home__title {
        margin: 0 0 6px;
        font-size: 32px;

        .demo-home__title img,
        .demo-home__title span {
          display: inline-block;
          vertical-align: middle;
        }
      }

      .item {
        font-size: 14px;
        line-height: 34px;

        a {
          text-decoration: underline;
        }

        .van-button {
          /* vant-ui 元素*/
          background: #ff5500;
        }
      }

      .logo {
        width: 120px;
        height: 120px;
        background: url($cdn+ '/weapp/logo.png') center / contain no-repeat;
      }

      .wechat {
        width: 200px;
        height: 200px;

        img {
          width: 100%;
          height: auto;
        }
      }
    }
  }
}
</style>
