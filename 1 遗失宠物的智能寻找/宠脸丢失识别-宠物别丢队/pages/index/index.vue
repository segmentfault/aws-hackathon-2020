<template>
	<view class="content">
		<view class="text-area">
			<text class="title">{{title}}</text>
		</view>
		<br>
		<br>
		请输入最后看见狗的位置:
		<br><br>
		<input type="text" style="border: 1px solid black;" value="北京天安门" />
		<br>
		<br>
		请输入狗的大小:
		<br><br>
		<input type="text" style="border: 1px solid black;" value="20" />
		<br>
		<view>
			<h3>预测位置(狗可能的位置)</h3>
		</view>
		<br>
		<map :scale="mapScale" id="home" @tap="tapMap" 
		@callouttap="callouttap" @markertap="markertap" 
		@controltap="controltap" :polyline="polyline" 
		:style="{'width': '100%', 'height': height + 'px'}" 
		:latitude="latitude" :longitude="longitude" 
		:markers="markers"> </map>
	</view>
</template>

<script>
	export default {
		data() {
  return {
      id:0, // 使用 marker点击事件 需要填写id
            title: '狗狗预测',
            latitude: 39.909,
            longitude: 116.39742,
            covers: [{
                latitude: 39.909,
                longitude: 116.39742,
                iconPath: '../../../static/location.png'
            }, {
                latitude: 39.90,
                longitude: 116.39,
                iconPath: '../../../static/location.png'
            }]
        }
		},
		onLoad() {

		},
		methods: {

		}
	}
</script>

<style>
	.content {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
	}

	.logo {
		height: 200rpx;
		width: 200rpx;
		margin-top: 200rpx;
		margin-left: auto;
		margin-right: auto;
		margin-bottom: 50rpx;
	}

	.text-area {
		display: flex;
		justify-content: center;
	}

	.title {
		font-size: 36rpx;
		color: #8f8f94;
	}
</style>
