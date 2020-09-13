import React from 'react'
import {Layout, Divider} from 'antd'
import CustomBreadcrumb from '@/components/CustomBreadcrumb'

const AboutView = () => (
  <Layout>
    <div>
      <CustomBreadcrumb arr={['关于']}></CustomBreadcrumb>
    </div>
    <div className='base-style'>
      <h3>关于作者</h3>
      <Divider/>
      <p>我是一名前端工作者，同时对AI有很高的兴趣，非常感谢aws这次举办的比赛</p>
    </div>
  </Layout>
)
export default AboutView
