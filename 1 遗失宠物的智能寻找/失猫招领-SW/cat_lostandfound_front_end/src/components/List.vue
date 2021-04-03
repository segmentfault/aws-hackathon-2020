<template>
  <van-list
    v-model="loading"
    :finished="finished"
    finished-text="没有更多了"
    @load="onload"
  >
    <div
      class="pet-item-wrapper"
      :class="{ last: index === data.length - 1 }"
      v-for="(item, index) in data"
      :key="item.post_id"
    >
      <div v-if="isFound(item.status)" class="overlay">
        <div class="overlay-tag">已完成</div>
      </div>
      <van-card
        @click="toDetail(item.post_id)"
        :thumb="showThumb(item.cover_path)"
        :title="item.title"
      >
        <template #desc>
          <div class="desc">{{ showDesc(item) }}</div>
        </template>
        <template #tag>
          <van-tag
            v-if="item.type !== -1"
            :type="type[item.type].color"
            size="medium"
          >
            {{ type[item.type].text }}
          </van-tag>
        </template>
        <template #tags>
          <van-tag
            v-if="item.cat_class !== -1"
            type="danger"
            style="margin-right: 6px;"
          >
            {{ cat.find((v) => v.value === item.cat_class).key }}
          </van-tag>
          <van-tag type="danger">
            {{ adult.find((v) => v.value === item.adult).key }}
          </van-tag>
        </template>
        <template #num>
          <span style="color: #969799">
            {{ showPublishDate(item) }}
          </span>
        </template>
      </van-card>
    </div>
  </van-list>
</template>

<script>
  import { cat, status, adult } from '../assets/enum.js'
  import { format, formatDistanceToNow } from 'date-fns'
  import { zhCN } from 'date-fns/locale'

  export default {
    props: {
      api: {
        type: Function,
      },
    },

    data() {
      return {
        type: [
          { text: '失踪', desc: '丢失于', color: 'warning' },
          { text: '招领', desc: '发现于', color: 'success' },
        ],
        cat,
        status,
        adult,

        loading: false,
        finished: false,

        data: [],
      }
    },

    methods: {
      isFound(v) {
        return v === 1
      },

      toDetail(v) {
        this.$router.push({ name: 'detail', params: { post_id: v } })
      },

      showDesc(v) {
        if (v.type === -1) return

        return `
          ${this.type[v.type].desc} ${format(v.lof_time, 'yyyy年MM月dd日')}
        `
      },

      showThumb(v) {
        return v !== void 0 && v !== null ? this.$imgServer + v : 'no-image'
      },

      showPublishDate(v) {
        return formatDistanceToNow(new Date(v.timestamp), {
          addSuffix: true,
          locale: zhCN,
        })
      },

      alertErrorMessage(message) {
        this.$dialog.alert({
          message,
        })
      },

      onload() {
        this.loading = true

        this.api()
          .then((response) => {
            if (response.success === false) {
              this.alertErrorMessage(response.msg)
              return
            }

            this.data = response.detail
          })
          .finally(() => {
            this.loading = false
            this.finished = true
          })
      },
    },
  }
</script>

<style lang="scss" scoped>
  .pet-item-wrapper {
    position: relative;
    margin-bottom: 16px;

    &.last {
      margin-bottom: 0;
    }

    .overlay {
      position: absolute;
      width: 100%;
      height: 100%;
      background-color: rgba(255, 255, 255, 0.6);
      z-index: 999;

      &-tag {
        display: flex;
        justify-content: center;
        align-items: center;
        position: absolute;
        top: 8px;
        left: 16px;
        padding: 0.8rem;
        width: 88px;
        height: 88px;
        background-color: rgba(30, 30, 30, 0.6);
        color: #fff;
        border-radius: 8px;
        text-align: right;
      }
    }
  }

  .desc {
    margin: 8px 0 4px;
  }
</style>
