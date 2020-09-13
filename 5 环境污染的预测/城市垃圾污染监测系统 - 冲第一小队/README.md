# 城市垃圾污染监测系统

## 作品介绍
对城市垃圾进行检测，使用了aws s3、aws SageMaker技术来进行机器学习，训练好模型并且部署模型到aws，通过endpoint来调用部署好的模型，使用Python tkinter技术做了个客户端可视化窗口，大大降低产品使用难度。

## 作品截图

- 首页
<p>
  <img src="./imgs/1.png" width="450" style="display:inline;" alt="">
</p>

- 检测结果
<p>
  <img src="./imgs/2.png" width="450" style="display:inline;" alt="">
</p>

- 检测结果
<p>
  <img src="./imgs/3.png" width="450" style="display:inline;" alt="">
</p>

## 安装、编译指南
- 安装
使用了Python技术，版本为Python3.7.7，
需要安装的包见requirements.txt

- 运行
直接运行mainUI.py即可
```
python mianUI.py
```

## 团队介绍
大家好，我是一名Python热爱者，Python能给我带来很多有趣的东西。

## 使用到的 AWS 技术
- aws s3
- aws SageMaker
- boto3
