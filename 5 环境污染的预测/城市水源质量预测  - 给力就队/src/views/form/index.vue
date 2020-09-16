<template>
  <div class="app-container">
    <div ref="trainData" class="train-data"></div>
    <el-button type="primary" class="predict-button" :loading="isLoading" @click="startPredict">预测下个48小时的PH值</el-button>
    <div ref="predictionData" class="train-data"></div>
  </div>
</template>

<script>
import TrainData from '../../assets/train.json'
import TestData from '../../assets/test.json'
import echarts from 'echarts'

export default {
  name: 'form',
  data() {
    return {
      isLoading: false
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.initChart()
    })
  },
  methods: {
    initChart() {
      this.chart = echarts.init(this.$refs.trainData, 'macarons')
      let xAxisData = []
      new Array(TrainData.target.length).fill(0).forEach((value, index) => {
        xAxisData.push(index + 1)
      })
      this.chart.setOption({
        title: {
          text: '某城市主要河道最近352小时的PH值',
          left: 'center',
          align: 'right'
        },
        toolbox: {
          feature: {
            dataZoom: {
              yAxisIndex: 'none'
            },
            restore: {},
            saveAsImage: {}
          }
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross'
          }
        },
        xAxis: {
          name: '小时',
          axisTick: {
            show: false
          },
          type: 'category',
          data: xAxisData
        },
        yAxis: {
          name: 'PH值',
          axisTick: {
            show: false
          },
          type: 'value'
        },
        dataZoom: [
          {
            show: true,
            realtime: true,
            start: 0,
            end: 50
          },
          {
            type: 'inside',
            realtime: true,
            start: 0,
            end: 50
          }
        ],
        series: [{
          data: TrainData.target,
          smooth: true,
          type: 'line',
          animationDuration: 2800,
          animationEasing: 'quadraticOut'
        }]
      })
    },
    startPredict() {
      this.isLoading = true
      let awsBody = {
        instances: [
          {
            start: '2020-07-01 00:00:00',
            target: TestData.target.slice(-48)
          }
        ], configuration: {
          num_samples: 100,
          output_types: [
            'quantiles'
          ],
          quantiles: [
            '0.1',
            '0.5',
            '0.9'
          ]
        }
      }

      let sagemakerruntime = new AWS.SageMakerRuntime({
        accessKeyId: 'AKIAQFNM7YIF6TDGUVMN',
        secretAccessKey: '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',
        region: 'cn-northwest-1'
      })
      let params = {
        Body: JSON.stringify(awsBody),
        EndpointName: 'hys-2020-09-15-13-23-44-033',
        Accept: '*/*',
        ContentType: 'application/json'
      }
      sagemakerruntime.invokeEndpoint(params, (err, data) => {
        this.isLoading = false
        if (err) {
          console.log(err, err.stack)
        } else {
          let response = JSON.parse(String.fromCharCode.apply(null, new Uint8Array(data.Body)))
          this.setPredictionOptions(response.predictions[0].quantiles['0.5'])
        }
      })
    },
    setPredictionOptions(data) {
      console.log(data)
      let xAxisData = []
      new Array(48).fill(0).forEach((value, index) => {
        xAxisData.push(index + 1)
      })
      this.predictionchart = echarts.init(this.$refs.predictionData, 'macarons')
      this.predictionchart.setOption({
        toolbox: {
          feature: {
            dataZoom: {
              yAxisIndex: 'none'
            },
            restore: {},
            saveAsImage: {}
          }
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross'
          }
        },
        xAxis: {
          name: '小时',
          axisTick: {
            show: false
          },
          type: 'category',
          data: xAxisData
        },
        yAxis: {
          name: 'PH值',
          axisTick: {
            show: false
          },
          type: 'value'
        },
        legend: {
          data: ['真实的下个48小时PH值', '预测的下个48小时PH值']
        },
        series: [{
          name: '真实的下个48小时PH值', itemStyle: {
            normal: {
              color: '#FF005A',
              lineStyle: {
                color: '#FF005A',
                width: 2
              }
            }
          },
          smooth: true,
          type: 'line',
          data: TestData.target.slice(-48),
          animationDuration: 1800,
          animationEasing: 'cubicInOut'
        }, {
          name: '预测的下个48小时PH值',
          itemStyle: {
            normal: {
              color: '#3888fa',
              lineStyle: {
                color: '#3888fa',
                width: 2
              },
              areaStyle: {
                color: '#f3f8ff'
              }
            }
          },
          data,
          smooth: true,
          type: 'line',
          animationDuration: 1800,
          animationEasing: 'quadraticOut'
        }]
      })
    }
  }
}
</script>

<style scoped>
.train-data {
  width: 100%;
  height: 350px;
}

.predict-button {
  margin-top: 20px;
  margin-bottom: 20px;
}
</style>

