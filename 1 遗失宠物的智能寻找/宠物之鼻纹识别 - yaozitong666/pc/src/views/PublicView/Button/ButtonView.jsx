import React, {Component} from 'react'
import CustomBreadcrumb from '@/components/CustomBreadcrumb'
import '@/style/view-style/button.scss'

import {Button, Col, Divider, Icon, Layout, Row, Upload, Modal} from 'antd'
import AWS from 'aws-sdk/dist/aws-sdk-react-native';

class ButtonView extends Component {
  state = {
    imgSrc: '',
    contents: '',
    visible: false
  }

  resMap = ['猫猫的鼻纹', '狗狗的鼻纹']

  /**
   * file图片文件转base64
   * @param {*} img file文件或者blob
   * @param {*} callback function (imgurl)通过参数获得base64
   */
  getBase64(img, callback) {
    const reader = new FileReader()
    reader.addEventListener('load', () => callback(reader.result))
    reader.readAsDataURL(img)
  }

  handleOk = e => {
    this.setState({
      visible: false,
    });
  };

  handleCancel = e => {
    this.setState({
      visible: false,
    });
  };

  render() {
    const {imgSrc, contents} = this.state
    return (
      <Layout className='button animated fadeIn'>
        <div>
          <CustomBreadcrumb arr={['宠物鼻纹', '识别']}></CustomBreadcrumb>
        </div>
        <div className='base-style'>
          <h3>介绍</h3>
          <Divider/>
          <p>猫猫和狗狗的鼻纹其实就相当于人类的指纹，具有不变的唯一性。世界上不会有两只鼻纹一模一样的猫猫和狗狗，而猫猫和狗狗在成长过程中，鼻纹也是不会发生变化的。所以，鼻纹就成了辨认猫猫和狗狗最重要的特征。</p>
        </div>
        <div>
          <Row gutter={8}>
            <Col span={24}>
              <div className='base-style'>
                <Upload showUploadList={false}
                        beforeUpload={() => {
                          return false
                        }}
                        onChange={(info) => {
                          this.getBase64(info.file, base64Img => {
                            this.setState({imgSrc: base64Img});
                            let sagemakerruntime = new AWS.SageMakerRuntime({
                              accessKeyId: 'AKIAQBHQUCTQ73EI6DGN',
                              secretAccessKey: '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',
                              region: 'cn-northwest-1'
                            });
                            let params = {
                              Body: new Buffer(base64Img.slice(22), 'base64'),
                              EndpointName: 'nose-endpoint',
                              Accept: '*/*',
                              ContentType: 'application/x-image',
                            };
                            sagemakerruntime.invokeEndpoint(params, (err, data) => {
                              if (err) console.log(err, err.stack);
                              else {
                                let res = JSON.parse(String.fromCharCode.apply(null, new Uint16Array(data.Body)));
                                let score = Math.max(...res)
                                let index = res.indexOf(score)
                                this.setState({visible: true, contents: `这是${this.resMap[index]}, 可信度为${score}`});
                              }
                            });
                          })
                        }}>
                  <Button>
                    <Icon type="upload"/> 点击上传宠物鼻纹
                  </Button>
                </Upload>
                <img src={imgSrc} alt=""/>
              </div>
            </Col>
          </Row>
          <Modal
            title="识别结果"
            visible={this.state.visible}
            onOk={this.handleOk}
            onCancel={this.handleCancel}
          >
            <p>{contents}</p>
          </Modal>
        </div>
      </Layout>
    )
  }
}

export default ButtonView
