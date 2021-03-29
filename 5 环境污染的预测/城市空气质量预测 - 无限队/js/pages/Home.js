import React, {Component} from 'react';
import {StyleSheet, View, ScrollView, Text, ToastAndroid} from 'react-native';
import {VictoryChart, VictoryLine, VictoryTheme, createContainer} from 'victory-native';
import TrainData from '../assets/train.json';
import AllData from '../assets/test.json';
import TestData from '../assets/testdata.json';
import AWS from 'aws-sdk/dist/aws-sdk-react-native';
import {Button} from 'react-native-paper';

const VictoryZoomVoronoiContainer = createContainer('zoom', 'voronoi');

class Home extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data_01: [],
      data_05: [],
      data_09: [],
    };
  }

  startPrediction = () => {
    let sagemakerruntime = new AWS.SageMakerRuntime({
      accessKeyId: 'AKIAQFGSUND4ZXHNRKUN',
      secretAccessKey: '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',
      region: 'cn-northwest-1',
    });
    let params = {
      Body: JSON.stringify(TestData),
      EndpointName: 'aqi-endpoint',
      Accept: '*/*',
      ContentType: 'application/json',
    };
    sagemakerruntime.invokeEndpoint(params, (err, data) => {
      if (err) {
        console.log(err, err.stack);
      } else {
        ToastAndroid.show('预测成功', ToastAndroid.SHORT);
        let resList = JSON.parse(String.fromCharCode.apply(null, new Uint16Array(data.Body)));
        let temp_01 = [], temp_05 = [], temp_09 = [];
        resList.predictions[0].quantiles['0.1'].forEach((eachPoint, index) => {
          temp_01.push({x: index + 1, y: eachPoint});
        });
        resList.predictions[0].quantiles['0.5'].forEach((eachPoint, index) => {
          temp_05.push({x: index + 1, y: eachPoint});
        });
        resList.predictions[0].quantiles['0.9'].forEach((eachPoint, index) => {
          temp_09.push({x: index + 1, y: eachPoint});
        });
        this.setState({
          data_01: temp_01,
          data_05: temp_05,
          data_09: temp_09,
        });
      }
    });
  };

  render() {
    let lineData = [];
    TrainData.target.forEach((eachPoint, index) => {
      lineData.push({x: index + 1, y: eachPoint});
    });
    // let actual_data = [];
    // AllData.target.forEach((eachPoint, index) => {
    //   if (index > 351) {
    //     actual_data.push({x: index + 1, y: eachPoint});
    //   }
    // });
    const {data_01, data_05, data_09} = this.state;
    return (
      <View style={styles.container}>
        <ScrollView>
          <Text style={styles.title}>原始数据</Text>
          <VictoryChart
            theme={VictoryTheme.grayscale}
            containerComponent={
              <VictoryZoomVoronoiContainer
                labels={({datum}) => `( ${datum.x} , ${datum.y} )`}
                dimension={'x'}
              />
            }
          >
            <VictoryLine
              style={{
                data: {stroke: '#c43a31'},
                parent: {border: '1px solid #ccc'},
              }}
              data={lineData}
            />
          </VictoryChart>

          {/*<Text style={styles.title}>真实48H后数据</Text>*/}
          {/*<VictoryChart*/}
          {/*  theme={VictoryTheme.grayscale}*/}
          {/*  containerComponent={*/}
          {/*    <VictoryZoomVoronoiContainer*/}
          {/*      labels={({datum}) => `( ${datum.x} , ${datum.y} )`}*/}
          {/*      dimension={'x'}*/}
          {/*    />*/}
          {/*  }*/}
          {/*>*/}
          {/*  <VictoryLine*/}
          {/*    style={{*/}
          {/*      data: {stroke: '#c43a31'},*/}
          {/*      parent: {border: '1px solid #ccc'},*/}
          {/*    }}*/}
          {/*    data={actual_data}*/}
          {/*  />*/}
          {/*</VictoryChart>*/}

          <Button onPress={this.startPrediction} color='black' icon={'emoticon-cool-outline'}>
            开始预测48H后数据
          </Button>

          <Text style={styles.title}>分位数为0.1</Text>
          <VictoryChart
            theme={VictoryTheme.grayscale}
            containerComponent={
              <VictoryZoomVoronoiContainer
                labels={({datum}) => `( ${datum.x} , ${datum.y} )`}
                dimension={'x'}
              />
            }
          >
            <VictoryLine
              style={{
                data: {stroke: '#c43a31'},
                parent: {border: '1px solid #ccc'},
              }}
              data={data_01}
            />
          </VictoryChart>

          <Text style={styles.title}>分位数为0.5</Text>
          <VictoryChart
            theme={VictoryTheme.grayscale}
            containerComponent={
              <VictoryZoomVoronoiContainer
                labels={({datum}) => `( ${datum.x} , ${datum.y} )`}
                dimension={'x'}
              />
            }
          >
            <VictoryLine
              style={{
                data: {stroke: '#c43a31'},
                parent: {border: '1px solid #ccc'},
              }}
              data={data_05}
            />
          </VictoryChart>

          <Text style={styles.title}>分位数为0.9</Text>
          <VictoryChart
            theme={VictoryTheme.grayscale}
            containerComponent={
              <VictoryZoomVoronoiContainer
                labels={({datum}) => `( ${datum.x} , ${datum.y} )`}
                dimension={'x'}
              />
            }
          >
            <VictoryLine
              style={{
                data: {stroke: '#c43a31'},
                parent: {border: '1px solid #ccc'},
              }}
              data={data_09}
            />
          </VictoryChart>
        </ScrollView>
      </View>
    );
  }
}

export default Home;

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
    marginLeft: 15,
    marginTop: 10,
  },
});
