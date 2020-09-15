# 狗不离 - 对不对

## 作品介绍
宠物的意外走失给很多饲养宠物家庭带来了困扰，本项目通过深度学习的算法能够对狗的面部特征进行识别。用户可以对自己的宠物进行注册，将面部数据储存在数据库中。而其他人可以将找到的动物拍照上传，系统会查找数据库中与之相似的狗的图片并交给上传者确认，如果上传者发现有相同的动物，可以向狗的主人发送通知。

## 作品功能

* 登录注册功能
* 上传基本信息
* 上传狗的图片发布丢失信息
* 上传狗的图片匹配数据库中的信息

## 作品截图
![注册界面](https://raw.githubusercontent.com/dythebs/aws-hackathon-2020/master/1%20%E9%81%97%E5%A4%B1%E5%AE%A0%E7%89%A9%E7%9A%84%E6%99%BA%E8%83%BD%E5%AF%BB%E6%89%BE/%E7%8B%97%E4%B8%8D%E7%A6%BB%20-%20%E5%AF%B9%E4%B8%8D%E5%AF%B9/images/%E6%B3%A8%E5%86%8C.png)
![发布丢失信息](https://github.com/dythebs/aws-hackathon-2020/blob/master/1%20%E9%81%97%E5%A4%B1%E5%AE%A0%E7%89%A9%E7%9A%84%E6%99%BA%E8%83%BD%E5%AF%BB%E6%89%BE/%E7%8B%97%E4%B8%8D%E7%A6%BB%20-%20%E5%AF%B9%E4%B8%8D%E5%AF%B9/images/%E6%B7%BB%E5%8A%A0.png?raw=true)
![搜索](https://raw.githubusercontent.com/dythebs/aws-hackathon-2020/master/1%20%E9%81%97%E5%A4%B1%E5%AE%A0%E7%89%A9%E7%9A%84%E6%99%BA%E8%83%BD%E5%AF%BB%E6%89%BE/%E7%8B%97%E4%B8%8D%E7%A6%BB%20-%20%E5%AF%B9%E4%B8%8D%E5%AF%B9/images/%E6%90%9C%E7%B4%A2.png)

## 技术路线
本项目的算法部分主要参考人脸识别的原理，通过神经网络生成狗的面部的embedding信息。同一只狗的不同图片向量距离尽可能接近。而不同的狗的距离尽可能远。将模型训练完成后部署到aws sagemaker的endpoint上。并通过lambda + api gateway封装成可以直接调用的Restful api。
应用部分采用前后端分离的架构，后端使用spring boot + mybatis框架，前端使用vue开发。

## 团队介绍
杨文武 244271172@qq.com

## 使用到的 AWS 技术
* EC2 作为web应用服务器
* RDS MySQL数据库
* S3 对象存储
* SegeMaker 深度学习模型训练、部署
* Lambda API Gateway 封装模型调用
