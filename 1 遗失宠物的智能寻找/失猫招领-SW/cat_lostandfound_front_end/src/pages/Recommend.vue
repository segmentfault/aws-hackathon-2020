<template>
  <div class="recommend">
    <div class="recommend-info van-hairline--bottom">
      <div class="recommend-info-content">
        <van-icon name="checked" color="#07c160" size="80" />
        <p>启事发布成功</p>
        <van-button type="default" @click="toMyPost">查看我的启事</van-button>
        <van-button type="default" style="margin-left: 8px;" @click="toResult"
          >回到首页</van-button
        >
      </div>
      <div class="recommend-info-footer">
        根据你填写的启事信息, 下面是与你发布较为相似的启事信息,
        你要寻找/招领的宠物可能已经被找到
      </div>
    </div>
    <div class="recommend-list van-hairline--top">
      <me-list :api="fetchPostByFilter"></me-list>
    </div>
  </div>
</template>
<script>
  import List from '../components/List.vue'

  export default {
    name: 'Recommend',

    components: {
      'me-list': List,
    },

    props: {
      filter: {
        type: Object,
        default: function() {
          return {
            cat_class: -1,
            type: -1,
            adult: -1,
            startTime: -1,
            endTime: -1,
          }
        },
      },
    },

    methods: {
      toMyPost() {
        this.$router.push({ name: 'my-post' })
      },

      toResult() {
        this.$router.push({ name: 'result' })
      },

      fetchPostByFilter() {
        return this.$request.getPostByFilter(this.filter)
      },
    },
  }
</script>
<style lang="scss" scoped>
  .recommend {
    &-info {
      padding: 16px;
      background-color: #fff;

      &-content {
        text-align: center;
      }

      &-footer {
        padding: 10px 16px;
        background-color: #fff;
        font-size: 12px;
        color: #888;
      }
    }

    &-list {
      margin-top: 16px;
    }
  }
</style>
