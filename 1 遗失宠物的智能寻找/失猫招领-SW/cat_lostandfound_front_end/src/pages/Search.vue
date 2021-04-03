<template>
  <van-form @submit="onSearchFilter">
    <van-cell
      :value="form.areaName"
      title="地区"
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
    <van-cell
      is-link
      :value="form.typeName"
      title="启事分类"
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
    <van-cell
      is-link
      :value="form.breedName"
      title="品种"
      @click="visible.breed = true"
    />
    <van-popup v-model="visible.breed" position="bottom">
      <van-picker
        show-toolbar
        title="选择品种"
        :columns="cat"
        @confirm="onConfirmBreed"
        @cancel="onCancel('breed')"
      />
    </van-popup>
    <van-cell
      is-link
      :value="form.statusName"
      title="状态"
      @click="visible.status = true"
    />
    <van-popup v-model="visible.status" position="bottom">
      <van-picker
        show-toolbar
        title="选择状态"
        :columns="status"
        @confirm="onConfirmStatus"
        @cancel="onCancel('status')"
      />
    </van-popup>
    <van-cell
      is-link
      :value="form.adultName"
      title="年龄"
      @click="visible.adult = true"
    />
    <van-popup v-model="visible.adult" position="bottom">
      <van-picker
        show-toolbar
        title="选择年龄"
        :columns="adult"
        @confirm="onConfirmAdult"
        @cancel="onCancel('adult')"
      />
    </van-popup>

    <van-cell
      is-link
      :value="form.dateName"
      title="日期区间"
      @click="visible.calendar = true"
    />
    <van-calendar
      v-model="visible.calendar"
      type="range"
      color="#07c160"
      :min-date="new Date(2017, 9, 12)"
      :max-date="new Date()"
      @confirm="onConfirmCalendar"
    />

    <div style="margin: 16px;">
      <van-button block type="primary" native-type="submit">
        确定
      </van-button>
    </div>
  </van-form>
</template>
<script>
  import area from '../assets/area.js'
  import { cat, type, adult, status } from '../assets/enum.js'
  import { format, add } from 'date-fns'

  export default {
    data() {
      return {
        active: 'filter',

        type: type.map((v) => v.key),
        cat: cat.map((v) => v.key),
        adult: adult.map((v) => v.key),
        status: status.map((v) => v.key),
        area,

        visible: {
          type: false,
          area: false,
          breed: false,
          status: false,
          adult: false,
          calendar: false,
        },

        form: {
          areaName: ['北京市', '北京市', '东城区'].join(' / '),
          areaValue: '110101',

          typeName: '',
          typeValue: -1,

          breedName: '',
          breedValue: -1,

          adultName: '',
          adultValue: -1,

          statusName: '',
          statusValue: -1,

          dateName: '',
          startTime: -1,
          endTime: -1,
        },
      }
    },
    methods: {
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

      onConfirmAdult(value) {
        this.visible.adult = false
        this.form.adultName = value
        this.form.adultValue = adult.find((v) => v.key === value).value
      },

      onConfirmStatus(value) {
        this.visible.status = false
        this.form.statusName = value
        this.form.statusValue = status.find((v) => v.key === value).value
      },

      onConfirmCalendar(date) {
        const [start, end] = date
        const formatString = 'yyyy年MM月dd日'

        this.form.startTime = start
        this.form.endTime = end

        this.form.dateName = [
          format(start, formatString),
          format(end, formatString),
        ].join(' - ')

        this.visible.calendar = false
      },

      onSearchFilter() {
        this.$router.push({
          name: 'result',
          params: {
            filter: {
              location: this.form.areaValue,
              cat_class: this.form.breedValue,
              type: this.form.typeValue,
              status: this.form.statusValue,
              adult: this.form.adultValue,
              startTime:
                this.form.startTime === -1 ? -1 : this.form.startTime.getTime(),
              endTime:
                this.form.endTime === -1
                  ? -1
                  : add(this.form.endTime, {
                      hours: 23,
                      minutes: 59,
                      seconds: 59,
                    }).getTime(),
            },
          },
        })
      },
    },
  }
</script>

<style lang="scss" scoped>
  .van-cell__value {
    flex: 3;
  }
</style>
