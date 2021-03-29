<template>
	<view>
		<view class="page-body">
			<view class="page-section page-section-gap">
				<map style="width: 100%; height: 300px;" :show-compass="compass" :latitude="latitude" :longitude="longitude" :markers="covers">
				</map>
			</view>
		</view>
		
		<button type="primary" @click="gomap()">获取宠物狗当前位置</button>
		<button type="primary" @click="goshibie()">宠脸识别</button>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				id:0, // 使用 marker点击事件 需要填写id
				title: 'map',
				latitude: 39.909,
				longitude: 116.29742,
				covers: [{
					title:'宠物当前位置',
					latitude: 39.909,
					longitude: 116.29742,
					iconPath: '../../static/gou.png'
				}]
				        
			}
		},
		onLoad() {

		},
		methods: {
			gomap(){
				let that = this
				that.latitude = 39.909;
				that.longitude = 116.29742;
				
			},
			goshibie(){
				let that = this;
				uni.navigateTo({
					url:'./shibie/shibie'
				})
			}
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
