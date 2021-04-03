<template>
  <div class="result">
    <div class="result-header van-hairline--bottom">
      <div class="result-header-title">发现</div>
      <div class="result-header-action">
        <van-icon
          @click="toSearch"
          name="filter-o"
          size="22px"
          style="margin-right: 16px;"
        />
        <van-icon @click="toPost" name="add-o" size="22px" />
      </div>
    </div>
    <div class="result-list">
      <me-list :api="fetchPostByFilter" />
    </div>
  </div>
</template>
<script>
  import List from '../components/List.vue'

  export default {
    name: 'Result',

    components: {
      'me-list': List,
    },

    props: {
      filter: {
        type: Object,
        default: function() {
          return {
            location: '110101',
            cat_class: -1,
            type: -1,
            status: -1,
            adult: -1,
            startTime: -1,
            endTime: -1,
          }
        },
      },
    },

    methods: {
      toSearch() {
        this.$router.push({ name: 'search' })
      },

      toPost() {
        this.$router.push({ name: 'post' })
      },

      fetchPostByFilter() {
        return this.$request.getPostByFilter(this.filter)
      },
    },
  }
</script>
<style lang="scss" scoped>
  .result {
    &-header {
      position: fixed;
      top: 0;
      left: 0;
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 8px 16px;
      width: 100%;
      height: 46px;
      background-color: #fff;
      z-index: 2;

      &-title {
        position: relative;
        padding-right: 8px;
      }
    }

    &-list {
      margin-top: 46px;
      margin-bottom: 50px;
    }
  }
</style>
