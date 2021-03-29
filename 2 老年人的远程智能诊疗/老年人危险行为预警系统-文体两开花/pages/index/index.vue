<template>
	<view class="content">
		<view class="headimg">
			<image src="../../static/下载.jpg" style="width: 200upx;height: 200upx;border: #FFFFFF 1rpx solid;border-radius: 200upx;"></image>
		</view>
		
		<view class="healthLine">
			<view class="tblock">
				<text class="textLine">21</text>
				<text class="textLite">℃</text>
				<p class="descript">体感温度</p>
				
			</view>
			<view class="tblock">
				<text class="textLine">88</text>
				<text class="textLite">%</text>
				<p class="descript">湿度</p>
			</view>
			<view class="tblock">
				<text class="textLine">85</text>
				<text class="textLite">优</text>
				<p class="descript">空气质量</p>
			</view>
		</view>
		
		<view class="total-descript">
			<text>今天天气不错~</text>
		</view>
		
		<view class="qiun-bg-white qiun-title-bar qiun-common-mt" >
			<view class="qiun-title-dot-light" style="color: #2FC25B;">陀螺仪记录表 正常行走</view>
		</view>
		<view class="qiun-charts" >
			<!--#ifdef MP-ALIPAY -->
			<canvas canvas-id="canvasArea" id="canvasArea" class="charts" :width="cWidth*pixelRatio" :height="cHeight*pixelRatio" :style="{'width':cWidth+'px','height':cHeight+'px'}" @touchstart="touchArea"></canvas>
			<!--#endif-->
			<!--#ifndef MP-ALIPAY -->
			<canvas canvas-id="canvasArea" id="canvasArea" class="charts" @touchstart="touchArea"></canvas>
			<!--#endif-->
		</view>
	</view>
</template>

<script>
	import uCharts from '@/components/u-charts/u-charts.js';
	import  { isJSON } from '@/common/checker.js';
	var _self;
	var canvaArea=null;
	var x=[0, 0, 0, 0, 0,0,0,0,0,0];
	var y=[0, 0, 0, 0, 0,0,0,0,0,0];
	var z=[0, 0, 0, 0, 0,0,0,0,0,0];
	export default {
		data() {
			return {
				cWidth:'',
				cHeight:'',
				pixelRatio:1,
				textarea:''
			}
		},
		onLoad() {
			_self = this;
			//#ifdef MP-ALIPAY
			uni.getSystemInfo({
				success: function (res) {
					if(res.pixelRatio>1){
						//正常这里给2就行，如果pixelRatio=3性能会降低一点
						//_self.pixelRatio =res.pixelRatio;
						_self.pixelRatio =2;
					}
				}
			});
			//#endif
			this.cWidth=uni.upx2px(750);
			this.cHeight=uni.upx2px(500);
			//this.getServerData();
			this.timer = setInterval(() => {
			               this.getServerData() 
			            }, 1000);
			
		},
		onShow() {
			let that = this;
			
		},
		methods: {
			getServerData(){
				
				let that = this;
				let Area={categories:['10s','9s','8s','7s','6s','5s','4s','3s','2s','1s'],series:[]};

				x.push(parseInt(Math.random()*10));
				x.shift()
				y.push(parseInt(Math.random()*10));
				y.shift()
				z.push(parseInt(Math.random()*10));
				z.shift()
				console.log(x);
				Area.series = [{
								"name": "X轴",
								"data": x,
								"color": "#facc14"
							  }, {
								"name": "Y轴",
								"data": y,
								"color": "#2fc25b"
							  }, {
								"name": "Z轴",
								"data": z,
								"color": "#1890ff"
							  }];
				
				_self.showArea("canvasArea",Area);
				
			},
			showArea(canvasId,chartData){
				canvaArea=new uCharts({
					$this:_self,
					canvasId: canvasId,
					type: 'area',
					fontSize:11,
					padding:[0,15,15,15],
					legend:{
						show:true,
						position:'top',
						float:'center',
						itemGap:30,
						padding:5,
						lineHeight:18,
						margin:0,
					},
					dataLabel:false,
					dataPointShape:true,
					background:'#FFFFFF',
					pixelRatio:_self.pixelRatio,
					categories: chartData.categories,
					series: chartData.series,
					animation: false,
					xAxis: {
						type:'grid',
						gridColor:'#CCCCCC',
						gridType:'dash',
						dashLength:8,
					},
					yAxis: {
						gridType:'dash',
						gridColor:'#CCCCCC',
						dashLength:8,
						splitNumber:5,
					},
					width: _self.cWidth*_self.pixelRatio,
					height: _self.cHeight*_self.pixelRatio,
					extra: {
						area:{
							type: 'curve',
							opacity:0.2,
							addLine:true,
							width:2,
							gradient:false
						}
					}
				});
				
			},
			touchArea(e) {
				canvaArea.touchLegend(e);
				canvaArea.showToolTip(e, {
					format: function (item, category) {
						return category + ' ' + item.name + ':' + item.data 
					}
				});
			},
			changeData(){
				if(isJSON(_self.textarea)){
					let newdata=JSON.parse(_self.textarea);
					canvaArea.updateData({
						series: newdata.series,
						categories: newdata.categories
					});
				}else{
					uni.showToast({
						title:'数据格式错误',
						image:'../../../static/images/alert-warning.png'
					})
				}
			}
		}
	}
</script>

<style>
	.body{
		background-color: #FFFFFF;
	}
	.headimg{
		margin-top: 120rpx;
		margin-bottom: 60rpx;
		text-align: center;
	}
	.healthLine{
		height: 150rpx;
		text-align: center;
	}
	.tblock{
		width: 33.333333333%;
		height: 150rpx;
		float: left;
	}
	.textLine{
		color: #007AFF;
		font-size: xx-large;
	}
	.textLite{
		color: #007AFF;
		font-size: small;
	}
	.descript{
		color: #9B9B9B;
		font-size: smaller;
	}
	.total-descript{
		height: 50rpx;
		width: 75%;
		margin: 0 auto;
		text-align: center;
		background-color: #EEEEEE;
		border: #FFFFFF solid 1rpx;
		border-radius: 200rpx;
		font-size: smaller;
	}
	.qiun-charts {
		width: 750upx;
		height: 500upx;
		background-color: #FFFFFF;
	}
	
	.charts {
		width: 750upx;
		height: 500upx;
		background-color: #FFFFFF;
	}
</style>
