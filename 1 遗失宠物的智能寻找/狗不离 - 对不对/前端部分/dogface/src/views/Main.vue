<template>
  <div>
    <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal">
      <el-menu-item index="0">
        DOG FACE
      </el-menu-item>
    </el-menu>
    <div style="width: 200px;">
      <el-menu
        default-active="1"
        class="el-menu-vertical-demo"
        style="height: 90vh;">
        <el-menu-item index="1" @click="fun1">
          <i class="el-icon-menu"></i>
          <span slot="title">相似图片搜索</span>
        </el-menu-item>
        <el-menu-item index="2" @click="fun2">
          <i class="el-icon-menu"></i>
          <span slot="title">注册</span>
        </el-menu-item>
      </el-menu>

    </div>
    <div class="container">
      <div style="display: inline-flex;height: 100%; width: calc(100% - 240px);" v-if="show1">
        <div class="left">
          <el-upload
            class="avatar-uploader"
            action="https://jsonplaceholder.typicode.com/posts/"
            :show-file-list="false"
            :on-success="handleAvatarSuccess"
            :before-upload="beforeAvatarUpload">
            <img v-if="imageUrl" :src="imageUrl" class="avatar">
            <i v-else class="el-icon-plus avatar-uploader-icon"></i>
            <div slot="tip" class="el-upload__tip" style="margin-left: 30px">点击上传待查询图片</div>
          </el-upload>
        </div>
        <div class="right" v-if="showimg">
          <el-row>
            <el-col :span="6" v-for="(o, index) in url" :key="index" :offset="index > 0 ? 3 : 0">
              <el-card :body-style="{ padding: '0px' }">
                <img :src="o.src" class="image">
                <div style="padding: 14px;">
                  <span>dog{{index}}</span>
                  <div class="bottom clearfix">
                    <time class="time">{{o.des}}</time>
                  </div>
                </div>
              </el-card>
            </el-col>
          </el-row>
        </div>
      </div>

      <div style="display: inline-flex;height: 100%; width: calc(100% - 240px);" v-if="show2">
        <div>
          <el-upload
            action="https://jsonplaceholder.typicode.com/posts/"
            list-type="picture-card"
            :on-preview="handlePictureCardPreview"
            :on-remove="handleRemove">
            <i class="el-icon-plus"></i>
            <div slot="tip" class="el-upload__tip" style="margin-left: 34px">点击上传图片</div>
          </el-upload>
          <el-dialog :visible.sync="dialogVisible">
            <img width="100%" :src="dialogImageUrl" alt="">
          </el-dialog>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
  export default {
    data() {
      return {
        imageUrl: '',
        url: [
          {
            src: require('../assets/0.1.jpg'),
            des:'DOG1'
          },
          {
            src: require('../assets/0.2.jpg'),
            des:'DOG2'
          },
          {
            src: require('../assets/0.3.jpg'),
            des:'DOG3'
          }
        ],
        currentDate: 'DOG',
        show1: false,
        show2: false,
        showimg: false,
        dialogImageUrl: '',
        dialogVisible: false,
        activeIndex: '1',
      };
    },
    methods: {
      fun1(){
        this.show1 = true;
        this.show2 = false;
      },
      fun2(){
        this.show1 = false;
        this.show2 = true;
      },
      handleAvatarSuccess(res, file) {
        this.imageUrl = URL.createObjectURL(file.raw);
        this.showimg = true;
      },
      beforeAvatarUpload(file) {
        const isJPG = file.type === 'image/jpeg';
        const isLt2M = file.size / 1024 / 1024 < 2;

        if (!isJPG) {
          this.$message.error('上传头像图片只能是 JPG 格式!');
        }
        if (!isLt2M) {
          this.$message.error('上传头像图片大小不能超过 2MB!');
        }
        return isJPG && isLt2M;
      },
      handleRemove(file, fileList) {
        console.log(file, fileList);
      },
      handlePictureCardPreview(file) {
        this.dialogImageUrl = file.url;
        this.dialogVisible = true;
      }
    }
  }
</script>

<style scoped>
  .avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 178px;
    height: 178px;
    line-height: 178px;
    text-align: center;
    border: 1px dashed #d9d9d9;
  }
  .avatar-uploader-icon:hover {
    border-color: #409EFF;
  }
  .avatar {
    width: 178px;
    height: 178px;
    display: block;
  }
  .left{
    margin-top: 19%;
    margin-left: 40px;
    width: 30%;
    height: 100%;
  }
  .right{
    margin-left: 40px;
    margin-top: 16%;
    width: 70%;
    height: 100%;
  }
  .time {
    font-size: 13px;
    color: #999;
  }

  .bottom {
    margin-top: 13px;
    line-height: 12px;
  }

  .button {
    padding: 0;
    float: right;
  }

  .image {
    width: 100%;
    display: block;
  }

  .clearfix:before,
  .clearfix:after {
    display: table;
    content: "";
  }

  .clearfix:after {
    clear: both
  }
  .el-menu-vertical-demo:not(.el-menu--collapse) {
    width: 200px;
    min-height: 400px;
    height: calc(100% - 60px);
  }
  .container{
    position: absolute;
    top: 80px;
    left: 240px;
    height: calc(100% - 100px);
    width: calc(100% - 240px);
    overflow-y: hidden;
    overflow-x: hidden;
  }

  .el-row {
    margin-bottom: 20px;
  }
  .el-col {
    border-radius: 4px;
    min-height: 1px;
  }
  .el-card__header{
    padding: 14px 20px;
  }
  .el-menu-item {
    width: 200px;
  }
  .el-header:focus {
    outline: none;
  }
  .el-upload{
    text-align: left;
  }
  .el-collapse-item__header{
    font-size: 16px;
    font-weight: bold;
  }
  .el-scrollbar__wrap {
    overflow-x: hidden;
  }
</style>
