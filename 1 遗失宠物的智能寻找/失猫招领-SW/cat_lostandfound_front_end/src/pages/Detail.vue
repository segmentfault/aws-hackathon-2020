<template>
  <div class="detail">
    <van-swipe
      v-if="photos.length > 0"
      @change="onChange"
      class="detail-photos"
      :height="216"
    >
      <van-swipe-item v-for="item in photos" :key="item.photo_id">
        <img
          style="width: auto; min-height: 100%; height: 100%;"
          :src="$imgServer + item.path"
        />
      </van-swipe-item>

      <template #indicator>
        <div class="detail-photos-indicator">{{ current + 1 }}/{{ total }}</div>
      </template>
    </van-swipe>
    <van-empty v-else description="没有相关的图片" />

    <van-cell
      title="启事分类"
      :value="
        detail.type !== -1 ? type.find((v) => v.value === detail.type).key : ''
      "
    />
    <van-cell
      :title="typeText[detail.type] + '日期'"
      :value="
        detail.lof_time !== -1
          ? new Date(detail.lof_time).toISOString().substring(0, 10)
          : ''
      "
    />
    <van-cell
      title="品种"
      :value="
        detail.cat_class !== -1
          ? cat.find((v) => v.value === detail.cat_class).key
          : ''
      "
    />
    <van-cell
      title="年龄"
      :value="
        detail.adult !== -1
          ? adult.find((v) => v.value === detail.adult).key
          : ''
      "
    />
    <van-cell
      title="状态"
      :value="
        detail.status !== -1
          ? status.find((v) => v.value === detail.status).key
          : ''
      "
    />
    <div v-if="detail.description" class="detail-description">
      {{ detail.description }}
    </div>

    <div style="margin: 16px;" v-if="isLoginUser">
      <van-button block type="danger" @click="onConfirmDelete">
        删除
      </van-button>
    </div>
  </div>
</template>

<script>
  import { cat, type, status, adult } from '../assets/enum.js'

  export default {
    name: 'Detail',

    props: {
      post_id: {
        type: [String, Number],
        required: true,
      },
    },

    data() {
      return {
        cat,
        type,
        typeText: ['丢失', '发现'],
        status,
        adult,

        photos: [],
        current: 0,
        total: 0,

        detail: {
          cat_class: -1,
          adult: -1,
          status: -1,
          type: 0,
          lof_time: -1,
          description: '',
        },
      }
    },

    computed: {
      isLoginUser() {
        return this.detail.user_id === JSON.parse(localStorage.getItem('token'))
      },
    },

    methods: {
      onChange(index) {
        this.current = index
      },

      onConfirmDelete() {
        this.$dialog
          .confirm({
            title: '提示',
            message: '确定要删除启事么?',
          })
          .then(() => {
            this.onDelete()
          })
      },

      async onDelete() {
        this.$toast.loading()

        const responsePhoto = await this.$request.getPostPhoto(this.post_id)
        await Promise.all([
          this.$request.deletePost(this.post_id),
          this.$request.deletePostPhoto(this.post_id),

          responsePhoto.detail.map((photo) =>
            this.$request.AWS_S3_DeletePhoto({ photoKey: photo.path })
          ),
        ])

        this.$toast.clear()
        this.$router.back()
      },

      async getPhotos() {
        const response = await this.$request.getPostPhoto(this.post_id)
        this.photos = response.detail
        this.total = this.photos.length
      },

      async getPost() {
        this.$toast.loading()
        const response = await this.$request.getPost(this.post_id)

        if (response.success === false) {
          this.$toast.clear()
          this.$dialog.alert({
            message: response.msg,
          })
        }

        this.$toast.clear()
        this.detail = response.detail
      },
    },

    created() {
      this.getPhotos()
      this.getPost()
    },
  }
</script>

<style lang="scss" scoped>
  .detail {
    &-photos {
      color: #fff;
      font-size: 20px;
      text-align: center;
      background: rgba(0, 0, 0, 0);

      &-indicator {
        position: absolute;
        right: 5px;
        bottom: 5px;
        padding: 2px 5px;
        font-size: 12px;
        color: #fff;
        background: rgba(0, 0, 0, 0.1);
      }
    }

    &-description {
      padding: 10px 16px;
      background-color: #fff;
      color: #969799;
      word-wrap: break-word;
      word-break: normal;
    }
  }
</style>
