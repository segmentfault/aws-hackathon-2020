<template>
  <div>
    <keep-alive>
      <router-view />
    </keep-alive>

    <van-tabbar route active-color="#07c160" inactive-color="#000">
      <van-tabbar-item to="/home/result" icon="search">
        发现
      </van-tabbar-item>
      <van-tabbar-item to="/home/profile" icon="user-o">
        我的
      </van-tabbar-item>
    </van-tabbar>
  </div>
</template>
