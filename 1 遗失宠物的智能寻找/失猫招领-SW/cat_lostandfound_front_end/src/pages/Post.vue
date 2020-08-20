<template>
  <div class="post">
    <van-form @submit="onSubmit">
      <!-- 标题 -->
      <van-field label="标题" name="title" v-model="form.title" />

      <!-- 发布类型 -->
      <van-field
        readonly
        clickable
        name="type"
        :value="form.typeName"
        label="启事分类"
        placeholder="点击选择启事分类"
        @click="visible.type = true"
      />
      <van-popup v-model="visible.type" position="bottom">
        <van-picker
          show-toolbar
          title="选择启事分类"
          :columns="type"
          @confirm="onConfirmType"
          @cancel="onCancel('type')"
        />
      </van-popup>

      <!-- 丢失时间 -->
      <van-field
        readonly
        clickable
        name="lostDate"
        :value="form.lostDateName"
        label="遗失日期"
        placeholder="点击选择遗失日期"
        @click="visible.lostDate = true"
      />
      <van-popup v-model="visible.lostDate" position="bottom">
        <van-datetime-picker
          v-model="form.lostDateValue"
          type="date"
          title="选择遗失日期"
          :min-date="minDate"
          :max-date="maxDate"
          :formatter="formatter"
          @confirm="onConfirmLostDate"
          @cancel="onCancel('lostDate')"
        />
      </van-popup>

      <!-- 已寻回 -->
      <!-- <van-field name="status" label="已寻回" input-align="right">
        <template #input>
          <van-switch
            v-model="form.status"
            size="20"
            :active-value="1"
            :inactive-value="0"
          />
        </template>
      </van-field> -->

      <!-- 已成年 -->
      <van-field name="adult" label="已成年" input-align="right">
        <template #input>
          <van-switch
            v-model="form.adult"
            size="20"
            :active-value="1"
            :inactive-value="0"
          />
        </template>
      </van-field>

      <!-- 地区 -->
      <van-field
        readonly
        clickable
        name="area"
        :value="form.areaName"
        label="地区"
        placeholder="点击选择省市区"
        @click="visible.area = true"
      />
      <van-popup v-model="visible.area" position="bottom">
        <van-area
          title="选择地区"
          :area-list="area"
          @confirm="onConfirmArea"
          @cancel="onCancel('area')"
        />
      </van-popup>

      <!-- 品种 -->
      <van-field
        readonly
        clickable
        name="breed"
        :value="form.breedName"
        label="品种"
        placeholder="智能识别品种"
        @click="visible.breed = true"
      >
        <template #right-icon>
          <div style="display:flex;">
            <van-loading v-if="predict.loading" size="24">
              {{ predict.text }}
            </van-loading>
            <van-icon
              v-else
              name="question-o"
              size="22"
              @click.stop="showTips"
            />
          </div>
        </template>
      </van-field>
      <van-popup v-model="visible.breed" position="bottom">
        <van-picker
          show-toolbar
          title="选择品种"
          :columns="cat"
          @confirm="onConfirmBreed"
          @cancel="onCancel('breed')"
        />
      </van-popup>

      <!-- 封面图片 -->
      <van-field
        name="uploader"
        style="padding-left: 15px; padding-right: 15px;"
      >
        <template #input>
          <van-uploader
            v-model="uploader"
            :after-read="afterRead"
            accept="image/png, image/jpeg"
            :max-count="8"
          />
        </template>
      </van-field>

      <!-- 详细描述 -->
      <van-field
        style="margin-top: 16px;"
        v-model="form.description"
        rows="6"
        autosize
        name="description"
        type="textarea"
        maxlength="150"
        placeholder="这里可以进一步详细描述"
        show-word-limit
      />

      <!-- 提交 -->
      <div style="margin: 16px;">
        <van-button block type="info" native-type="submit">
          提交
        </van-button>
      </div>
    </van-form>
  </div>
</template>
<script>
  import area from '../assets/area.js'
  import { cat, type } from '../assets/enum.js'

  function getPredictClass(photos) {
    const dict = {}
    let max = -1
    let output = -1

    photos.forEach(({ breed }) => {
      if (dict[breed] === void 0) dict[breed] = 1
      else dict[breed]++

      max = Math.max(max, dict[breed])
    })

    for (const key in dict) {
      if (max === dict[key]) {
        output = key
        break
      }
    }

    return Number(output)
  }

  const now = new Date()

  export default {
    data() {
      return {
        S3_Photos: [],

        predict: {
          loading: false,
          text: '',
        },

        area,

        type: type.map((v) => v.key),
        cat: cat.map((v) => v.key),

        isSubmit: false,

        post_id: -1,

        show: false,

        minDate: new Date(2010, 0, 1),
        maxDate: new Date(),

        uploader: [],

        visible: {
          tips: false,
          type: false,
          area: false,
          breed: false,
          lostDate: false,
        },

        form: {
          typeName: '',
          typeValue: -1,

          areaName: ['北京市', '北京市', '东城区'].join(' / '),
          areaValue: '110101',

          breedName: '',
          breedValue: -1,

          lostDateName: `${now.getFullYear()}年${now.getMonth() +
            1}月${now.getDate()}日`,
          lostDateValue: now,

          title: '',
          adult: 0,
          description: '',
        },
      }
    },

    methods: {
      showTips() {
        this.$dialog.alert({
          title: '提示',
          message: '人工智能预测猫的品种，如果您认为预测结果有误，可以手动选择',
        })
      },

      async afterRead({ file }) {
        this.predict.loading = true
        this.predict.text = '正在上传...'

        const response = await this.$request.AWS_S3_Upload({
          post_id: this.post_id,
          file: file,
        })

        this.predict.text = '识别中...'

        // 部署时需要添加http://18.181.212.95:5000
        const breed = await fetch(
          'http://18.181.212.95:5000/classify/' + response.key
        ).then((response) => response.json())

        // 开发时不用添加http://18.181.212.95:500这个地址, 会自动代理
        // const breed = await fetch(
        //   '/classify/' + response.key
        // ).then((response) => response.json())

        this.predict.loading = false

        this.S3_Photos.push({ key: response.key, breed: breed })

        const predictClass = getPredictClass(this.S3_Photos)

        this.form.breedName = cat.find((v) => v.value === predictClass).key
        this.form.breedValue = predictClass
      },

      formatter(type, val) {
        if (type === 'year') return `${val}年`
        else if (type === 'month') return `${val}月`
        else if (type === 'day') return `${val}日`

        return val
      },

      onCancel(type) {
        this.visible[type] = false
      },

      onConfirmType(value) {
        this.visible.type = false
        this.form.typeName = value
        this.form.typeValue = type.find((v) => v.key === value).value
      },

      onConfirmArea(values) {
        this.visible.area = false
        this.form.areaName = values.map((item) => item.name).join(' / ')
        this.form.areaValue = values[2].code
      },

      onConfirmBreed(value) {
        this.visible.breed = false
        this.form.breedName = value
        this.form.breedValue = cat.find((v) => v.key === value).value
      },

      onConfirmLostDate(values) {
        this.visible.lostDate = false
        this.form.lostDateName = `${values.getFullYear()}年${values.getMonth() +
          1}月${values.getDate()}日`
        this.form.lostDateValue = values
      },

      async addPost() {
        return await this.$request.addPost()
      },

      async deletePost() {
        const responsePhoto = await this.$request.getPostPhoto(this.post_id)

        return await Promise.all([
          this.$request.deletePost(this.post_id),
          this.$request.deletePostPhoto(this.post_id),

          responsePhoto.detail.map((photo) =>
            this.$request.AWS_S3_DeletePhoto({ photoKey: photo.path })
          ),
        ])
      },

      async onSubmit(values) {
        this.$toast.loading()

        const responsePhoto = await Promise.all(
          this.S3_Photos.map((photo, index) =>
            this.$request.addPostPhoto({
              post_id: this.post_id,
              path: photo.key,
              cat_class: photo.breed,
              photo_index: index + 1,
            })
          )
        )
        console.log(responsePhoto)
        if (responsePhoto.length > 0 && responsePhoto[0].success === true) {
          this.cover_path = responsePhoto[0].detail.path
        }

        const responsePost = await this.$request.updatePost({
          post_id: this.post_id,

          title: values.title,
          description: values.description,
          adult: values.adult,
          cover_path: this.cover_path,
          type: this.form.typeValue,
          location: this.form.areaValue,
          cat_class: this.form.breedValue,
          lof_time: this.form.lostDateValue.getTime(),
        })

        if (responsePost.success === false) {
          this.$toast.clear()
          this.$dialog.alert({
            title: '出错了',
            message: responsePost.msg,
          })

          return
        }

        this.$toast.clear()

        this.isSubmit = true
        this.$router.push({
          name: 'recommend',
          params: {
            filter: {
              location: this.form.areaValue,
              cat_class: this.form.breedValue,
              type: +!this.form.typeValue,
              adult: values.adult,
              status: 0,
              startTime: -1,
              endTime: -1,
            },
          },
        })
      },
    },

    async created() {
      this.$toast.loading()

      const response = await this.addPost()

      if (response.success === false) {
        this.$toast.clear()
        this.$dialog.alert({
          message: response.msg,
        })
        return
      }

      this.$toast.clear()
      this.post_id = response.detail.post_id
    },

    beforeRouteLeave(to, from, next) {
      if (this.isSubmit === true) {
        next()
        return
      }

      this.$dialog
        .confirm({
          title: '温馨提示',
          message: '离开将放弃当前编辑的内容',
        })
        .then(() => {
          this.deletePost()
          next()
        })
        .catch(() => {
          next(false)
        })
    },
  }
</script>
