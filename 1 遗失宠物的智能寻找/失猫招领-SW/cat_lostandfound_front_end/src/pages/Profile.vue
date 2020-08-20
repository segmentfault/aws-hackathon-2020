<template>
  <div class="profile">
    <div class="profile-info">
      <van-image
        round
        cover
        width="7rem"
        height="7rem"
        src="https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1599817787893&di=7cc94c02e11ea0bc0de7cc218243315f&imgtype=0&src=http%3A%2F%2Fpic.90sjimg.com%2Fdesign%2F00%2F67%2F59%2F63%2F58e89bec9af5e.png"
      />
      <div class="profile-info-email">
        {{ email }}
      </div>
    </div>
    <div class="">
      <van-cell title="我发布的信息" icon="records" is-link to="/my-post" />
    </div>
  </div>
</template>
<script>
  export default {
    data() {
      return {
        email: JSON.parse(localStorage.getItem('email')),
      }
    },
  }
</script>
<style lang="scss" scoped>
  .profile {
    &-info {
      margin: 1.5rem;
      padding: 1.25rem;
      height: 200px;
      background-color: #19f;
      border-radius: 12px;
      box-shadow: 0 8px 12px #ebedf0;
      text-align: center;

      &-email {
        margin-top: 1rem;
        font-size: 20px;
        color: #fff;
        border-color: #fff;
      }
    }
  }
</style>
