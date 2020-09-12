//index.js
//获取应用实例
var app = getApp()
Page({
  data: {
    motto: '快绑定宠物项圈，防止丢失吧',
    userInfo: {},
    appInfo:{
      logoUrl:'../../image/logo.png',
      title:'让你的宝贝永远不会走丢'
    }
  },
  //事件处理函数
  bindViewTap: function() {
    wx.navigateTo({
      url: '../location/location'
    })
  },
  onLoad: function () {
    console.log('onLoad')
    var that = this
    that.setData({
        appInfo:this.data.appInfo
    })
  	//调用应用实例的方法获取全局数据
    // app.getUserInfo(function(userInfo){
    //   //更新数据
    //   that.setData({
    //     userInfo:userInfo
    //   })
    //   that.update()
    // })
  }
})
