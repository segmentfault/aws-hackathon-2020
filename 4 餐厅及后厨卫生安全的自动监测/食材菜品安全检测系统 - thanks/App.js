/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 *
 * @format
 * @flow strict-local
 */
import React, {Component} from 'react';
import {
  DrawerLayoutAndroid,
  StatusBar,
  StyleSheet,
  Text,
  View,
  Image,
  TouchableOpacity,
  Alert,
  ToastAndroid,
  PermissionsAndroid,
  Modal,
  Button,
} from 'react-native';
import MaterialIcons from 'react-native-vector-icons/MaterialIcons';
import Foundation from 'react-native-vector-icons/Foundation';
import ImagePicker from 'react-native-image-picker';
import AWS from 'aws-sdk/dist/aws-sdk-react-native';
import {Buffer} from 'buffer';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      modalVisible: false,
      result: '',
      imagePath: '',
    };
    this.resMap = ['这是：新鲜水果蔬菜', '注意！这是腐烂水果蔬菜！'];
  }

  componentDidMount(): * {
    StatusBar.setBackgroundColor('#ffffff');
    StatusBar.setBarStyle('dark-content');
    this.requestExternalStoragePermission();
  }

  requestExternalStoragePermission = async () => {
    try {
      const granted = await PermissionsAndroid.requestMultiple(
        [PermissionsAndroid.PERMISSIONS.WRITE_EXTERNAL_STORAGE, PermissionsAndroid.PERMISSIONS.CAMERA, PermissionsAndroid.PERMISSIONS.RECORD_AUDIO],
      );
      let deniedPerms = '';
      Object.keys(granted).forEach(eachPermissions => {
        if (granted[eachPermissions] === PermissionsAndroid.RESULTS.DENIED) {
          switch (eachPermissions) {
            case PermissionsAndroid.PERMISSIONS.WRITE_EXTERNAL_STORAGE:
              deniedPerms += ' 读取存储';
              break;
            case  PermissionsAndroid.PERMISSIONS.CAMERA:
              deniedPerms += ' 相机';
              break;
            case  PermissionsAndroid.PERMISSIONS.RECORD_AUDIO:
              deniedPerms += ' 麦克风';
              break;
          }
        }
      });
      if (deniedPerms) {
        Alert.alert(
          '警告',
          '获取' + deniedPerms + ' 权限失败，这将导致应用核心功能无法使用！',
          [
            {text: '确定'},
          ],
          {cancelable: false},
        );
      }
    } catch (err) {
      ToastAndroid.show('获取权限失败 ' + JSON.stringify(err) + ' 这将导致应用核心功能无法使用！', ToastAndroid.LONG);
    }
  };

  openDrawer = () => {
    this.drawerRef.openDrawer();
  };

  
  render() {
    const navigationView = (
      <View style={styles.navigationView}>
        <Text style={styles.title}>关于作者</Text>
        <Text style={styles.content}>专业是软件工程，对APP开发有一定的经验，对机器学习有浓厚的兴趣，通过这次比赛把ai应用到自己生活中.</Text>
      </View>
    );

    const {modalVisible, imagePath, result} = this.state;

    return (
      <DrawerLayoutAndroid ref={ref => this.drawerRef = ref}
                           drawerWidth={300}
                           drawerPosition={'right'}
                           renderNavigationView={() => navigationView}>
        <View style={styles.container}>
          <View style={styles.titleWrap}>
            <Text style={styles.title}>食材菜品安全检测系统</Text>
            <MaterialIcons.Button name="menu-open"
                                  color='#3e3f68'
                                  backgroundColor="#ffffff"
                                  onPress={this.openDrawer}/>
          </View>
          <View style={styles.introductionView}>
            <Text style={styles.subtitle}>介绍</Text>
            <Text style={styles.content}>近年来，多家知名连锁餐饮品牌屡次被媒体曝出后厨卫生存在隐患，为食品安全加上人工智能的助力，情况或有改善。</Text>
            <Text style={styles.content}>通过AWS
              SegaMaker机器学习，训练并部署可识别新鲜水果蔬菜和腐烂水果蔬菜的模型，通过aws-sdk本地调用线上模型，给餐厅的视频监控加上一套有力的防护盾。</Text>
          </View>
          <View style={[styles.introductionView, {flexDirection: 'row'}]}>
            <View style={{flex: 1, alignItems: 'center', justifyContent: 'space-between'}}>
              <Image source={require('./images/scsg.jpg')} style={{width: '100%'}} resizeMode={'contain'}/>
              <Text>新鲜水果蔬菜</Text>
            </View>
            <View style={{flex: 1, alignItems: 'center', justifyContent: 'space-between'}}>
              <Image source={require('./images/flsgsc.jpg')} style={{width: '100%', marginTop: 50}}
                     resizeMode={'contain'}/>
              <Text>腐烂水果蔬菜</Text>
            </View>
          </View>
          <View style={styles.introductionView}>
            <TouchableOpacity onPress={this.selectPicToAWS}>
              <View style={{justifyContent: 'center', alignItems: 'center', paddingVertical: 10}}>
                <Foundation name="upload-cloud" size={50} color={'#009688'}/>
                <Text style={{marginTop: 10}}>请选择或拍摄图片</Text>
              </View>
            </TouchableOpacity>
          </View>
          <Modal animationType="fade"
                 statusBarTranslucent
                 visible={modalVisible}>
            <View style={{flex: 1, justifyContent: 'center', alignItems: 'center'}}>
              <Image source={{uri: 'file://' + imagePath}} style={{width: 500, height: 500, marginBottom: 15}}/>
              <Text>{result}</Text>
              <Button title={'确定'} onPress={() => {
                this.setState({modalVisible: false});
              }}/>
            </View>
          </Modal>
        </View>
      </DrawerLayoutAndroid>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  titleWrap: {
    flexDirection: 'row',
    paddingTop: 10,
    paddingLeft: 10,
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: '#ffffff',
    elevation: 10,
    paddingBottom: 15,
  },
  title: {
    fontSize: 25,
    color: '#000000',
    fontWeight: 'bold',
  },
  navigationView: {
    paddingTop: 10,
    paddingLeft: 10,
    paddingRight: 10,
  },
  content: {
    fontSize: 16,
    marginTop: 10,
  },
  subtitle: {
    fontSize: 20,
    fontWeight: 'bold',
  },
  introductionView: {
    marginTop: 10,
    paddingTop: 10,
    marginHorizontal: 15,
    paddingHorizontal: 10,
    paddingBottom: 10,
    backgroundColor: '#ffffff',
    elevation: 8,
    borderRadius: 8,
  },
});

export default App;
