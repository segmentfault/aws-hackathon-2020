<template>
  <div class="login">
    <div class="login-header">
      <div class="login-header-logo">
        <img
          :src="logo"
          style="display: inline-block; width: 80px; height: 80px;"
        />
        <!-- <svg
          t="1598682564531"
          class="icon"
          viewBox="0 0 1024 1024"
          version="1.1"
          xmlns="http://www.w3.org/2000/svg"
          p-id="1354"
          width="64"
          height="64"
        >
          <path
            d="M989.456194 235.835976l-104.562214-42.185733c-6.38522-33.753801-32.035606-60.778221-65.043725-69.165829l-5.655183-65.161053a23.465488 23.465488 0 0 0-40.76216-13.729918l-27.355544 30.171403-16.783039-58.744545a23.468095 23.468095 0 0 0-21.747292-17.004657c-10.163164-0.31548-19.405959 5.88723-22.876244 15.455934l-144.797704 399.460824c-104.160694 27.047886-195.115532 93.700301-250.981645 184.397019-51.170407 83.073042-67.064365 178.249061-44.7539 267.991516 13.038989 52.45058 37.795079 87.012637 63.119555 109.675083h-19.916984l-0.563172 0.007822c-94.213934 2.297011-181.5238-51.266877-222.293782-136.378809-5.597823-11.68842-19.611933-16.621387-31.300354-11.026172a23.465488 23.465488 0 0 0-11.023565 31.300354c47.739232 99.665749 148.818125 163.103392 258.866049 163.103392h448.005704a23.465488 23.465488 0 0 0 23.465487-23.465488c0-63.163879-50.380403-91.953425-94.844895-102.520717 20.790422-40.53272 22.586836-76.179403 20.229858-99.498883l6.132314-0.818685 140.644313 215.655656a23.470703 23.470703 0 0 0 19.656258 10.64551h85.401339a23.465488 23.465488 0 0 0 19.851803-35.972593c-0.907332-1.439217-89.080207-141.436925-136.480492-219.816869V373.925158c6.977072 0.803041 14.811937 1.207169 21.731649 1.207169 68.073381 0 132.095054-38.405182 166.565855-106.502028 0.02868-0.054753 0.912547-1.900705 1.05334-2.255294a23.462881 23.462881 0 0 0-12.98163-30.539029z"
            fill="#333333"
            p-id="1355"
          ></path>
        </svg> -->
      </div>
      <h1 class="login-header-title">失猫招领</h1>
    </div>
    <div class="login-form">
      <van-form @submit="onSubmit">
        <van-field
          v-model="email"
          name="email"
          label="邮箱"
          placeholder="邮箱"
          :rules="[{ required: true, message: '请填写邮箱' }]"
        />
        <van-field
          v-model="password"
          type="password"
          name="password"
          label="密码"
          placeholder="密码"
          :rules="[{ required: true, message: '请填写密码' }]"
        />
        <div style="margin: 16px;">
          <van-button block type="primary" native-type="submit">
            登录
          </van-button>
        </div>
      </van-form>
    </div>
    <div class="login-join">
      <router-link to="/join">创建账号</router-link>
    </div>
  </div>
</template>

<script>
  import logo from '../assets/cat.svg'

  export default {
    name: 'login',

    data() {
      return {
        logo: logo,

        email: '',
        password: '',
      }
    },

    methods: {
      async onSubmit(values) {
        try {
          this.$toast.loading()

          const response = await this.$request.login(values)

          if (response.success === false) {
            this.$dialog.alert({ message: response.msg })
            return
          }

          localStorage.setItem('token', JSON.stringify(response.detail.id))
          localStorage.setItem('email', JSON.stringify(response.detail.email))

          this.$router.push({ name: 'result' })
        } catch (error) {
          console.error(error)
          this.$dialog.alert({ message: error })
        } finally {
          this.$toast.clear()
        }
      },
    },
  }
</script>

<style lang="scss" scoped>
  .login {
    margin: 0 auto;
    width: 320px;

    &-header {
      margin-bottom: 1.25rem;
      text-align: center;

      &-logo {
        padding: 1.5rem 0 0.75rem;
      }

      &-title {
        font-weight: 300;
        color: #333;
      }
    }

    &-form {
      margin-top: 1.25rem;

      &-field {
        margin-top: 5px;
        margin-bottom: 15px;
      }

      &-button {
        margin-top: 1.5rem;
      }
    }

    &-join {
      padding: 1rem 0.25rem;
      text-align: center;
    }
  }
</style>
