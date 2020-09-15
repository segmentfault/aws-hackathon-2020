<template>
  <div class="pet-container">
    <van-grid :column-num="3">
      <van-grid-item v-for="imgObj in imgList" :key="imgObj.name">
        <van-image :src="imgObj.src"/>
        <span class="name">{{ imgObj.name }}</span>
      </van-grid-item>
    </van-grid>
    <div class="upload-wrap">
      <span class="select-pic-span">请选择宠物图片</span>
      <van-uploader :after-read="afterRead"/>
    </div>

    <van-dialog v-model="show" :title="title">
      <div class="img-wrap">
        <img :src="fileContent" alt="图片">
      </div>
    </van-dialog>
  </div>
</template>

<script>
export default {
  name: "pet",
  data() {
    return {
      imgList: [
        {
          src: require('../../assets/Abyssinian.jpg'),
          name: '阿比西尼亚'
        },
        {
          src: require('../../assets/Bengal.jpg'),
          name: '孟加拉'
        },
        {
          src: require('../../assets/Birman.jpg'),
          name: '比尔曼'
        },
        {
          src: require('../../assets/american_bulldog.jpg'),
          name: '美国斗牛犬1'
        },
        {
          src: require('../../assets/american_pit_bull_terrier.jpg'),
          name: '美国斗牛犬2'
        },
        {
          src: require('../../assets/beagle.jpg'),
          name: '小猎犬'
        },
      ],
      show: false,
      title: '',
      fileContent: '',
      petMap: ['阿比西尼亚', '孟加拉', '比尔曼', '美国斗牛犬1', '美国斗牛犬2', '小猎犬']
    }
  },
  methods: {
    afterRead(file) {
      this.fileContent = file.content
      this.$toast.loading({
        duration: 0, // 持续展示 toast
        message: '加载中...',
        forbidClick: true,
      });
      this.awsSageMaker(this.fileContent)
    },
    awsSageMaker(base64Img) {
      let sagemakerruntime = new AWS.SageMakerRuntime({
        accessKeyId: 'AKIAXCK4VB63DMRQNC6O',
        secretAccessKey: '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',
        region: 'cn-northwest-1'
      });
      let params = {
        Body: new Buffer(base64Img.slice(22), 'base64') /* Strings will be Base-64 encoded on your behalf */, /* required */
        EndpointName: 'my-dog-and-cat-endpoint', /* required */
        Accept: '*/*',
        ContentType: 'application/x-image',
      };
      sagemakerruntime.invokeEndpoint(params, (err, data) => {
        if (err) console.log(err, err.stack); // an error occurred
        else {
          let resultArr = JSON.parse(String.fromCharCode.apply(null, new Uint16Array(data.Body)));
          let score = Math.max(...resultArr)
          let petIndex = resultArr.indexOf(score)
          this.title = `这是亲爱的${this.petMap[petIndex]}，置信度为 ${score}`
          this.$toast.clear();
          this.show = true
        }           // successful response
      });
    }
  },
}
</script>

<style scoped>
.pet-container {
  height: 100vh;
}

.name {
  margin-top: 10px;
  color: #646566;
  font-size: 12px;
}

.upload-wrap {
  background-color: #ffffff;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding-top: 20px;
  padding-bottom: 20px;
}

.select-pic-span {
  font-size: 15px;
  color: #646566;
  margin-bottom: 10px;
}

.img-wrap {
  display: flex;
  flex: 1;
  justify-content: center;
  align-items: center;
}
</style>
