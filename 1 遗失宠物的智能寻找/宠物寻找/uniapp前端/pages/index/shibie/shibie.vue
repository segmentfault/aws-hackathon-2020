<template>
	<view>
		
	<camera device-position="back" flash="auto" @error="error" style="width: 100%; height: 500upx;">
		<cover-image src="../../../static/scan-img.png" class="scan-img"></cover-image>
	</camera>
	<view class="scan-text" style="text-align: center;">请将宠物面部放置白色框内</view>
	<button type="primary" @click="takePhoto">拍照识别</button>
	<image mode="widthFix" class="photos-box" :src="src"></image>
		
	</view>
</template>

<script>
	export default {
		data() {
			return {
				
			}
		},
		methods: {
			takePhoto() {
				const ctx = uni.createCameraContext();
				ctx.takePhoto({
					quality: 'high',
					success: (res) => {
						this.src = res.tempImagePath
						/* 返回调用页面并把图片URL传递过去 */
						/* let pages = getCurrentPages();
						let prevPage = pages[pages.length - 2]; 
						prevPage.setData({
							"image": res.tempImagePath,
						})
						uni.navigateBack(); */
						
						/* 调用页面获取图片URL方法 */
						/* let pages = getCurrentPages();
						let currPage = pages[pages.length-1];
						if(typeof(currPage.data.image) != undefined && currPage.data.image != null){
							console.log('获取图片：', currPage.data.image)
						} */
					}
				});
			},
			error(e) {
				console.log(e.detail);
			}
		}
	}
</script>

<style>

</style>
