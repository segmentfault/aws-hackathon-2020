# 赛题一：遗失宠物的智能寻找

* **作品介绍：**

  伴随着人们物质生活水平的提高，宠物狗在人们生活中扮演着越来越重要的角色，它们不仅是家庭的宠物，很多人也将他们视作家庭成员之一，给予百般宠爱和呵护。然而即便如此，意外还是难免发生——宠物的意外走失给很多宠物家庭带来了困扰，满大街发传单、贴广告不仅浪费时间，成效也甚微。在实际的生活中，宠物的种类多种多样，每种宠物也都有着不少的品种。以宠物狗为例，有很多品种的狗狗长相都相当接近，连经常接触狗的专家也不太好分辨。所以，当宠物丢失的时候，确认宠物的品种就变成了一大难题。所以为了提高辨别宠物种类的能力，本项目以常见宠物种类——狗做为研究对象，使用[斯坦福的犬类数据集](http://vision.stanford.edu/aditya86/ImageNetDogs/)（包括常见的120个品种的20580张狗的图片）进行训练，得到了一个识别率颇高的犬类分类模型。该模型使用四种网络对宠物狗图片进行特征提取，然后将提取到的特征进行融合，使用DNN网络进行分类。实验证明，该方法能有效地对宠物狗进行分类。

* **作品截图：**

  1.预测结果和实际结果的对比（每一个数字代表宠物狗的一个种类）

  ![1](https://github.com/ZxfBugProgrammer/aws-hackathon-2020/blob/master/1%20%E9%81%97%E5%A4%B1%E5%AE%A0%E7%89%A9%E7%9A%84%E6%99%BA%E8%83%BD%E5%AF%BB%E6%89%BE/%E7%8B%97%E7%8B%97%E7%A7%8D%E7%B1%BB%E8%AF%86%E5%88%AB%20-%20Sunburst/src/1.png)

  2.预测的正确率

  ![2](https://github.com/ZxfBugProgrammer/aws-hackathon-2020/blob/master/1%20%E9%81%97%E5%A4%B1%E5%AE%A0%E7%89%A9%E7%9A%84%E6%99%BA%E8%83%BD%E5%AF%BB%E6%89%BE/%E7%8B%97%E7%8B%97%E7%A7%8D%E7%B1%BB%E8%AF%86%E5%88%AB%20-%20Sunburst/src/2.png)

  3.以概率的形式输出预测结果

  ![3](https://github.com/ZxfBugProgrammer/aws-hackathon-2020/blob/master/1%20%E9%81%97%E5%A4%B1%E5%AE%A0%E7%89%A9%E7%9A%84%E6%99%BA%E8%83%BD%E5%AF%BB%E6%89%BE/%E7%8B%97%E7%8B%97%E7%A7%8D%E7%B1%BB%E8%AF%86%E5%88%AB%20-%20Sunburst/src/3.png)

* **安装、编译指南：**

  1.下载[斯坦福的犬类数据集](http://vision.stanford.edu/aditya86/ImageNetDogs/)（下载images.tar文件）存放到 “狗狗种类识别 - Sunburst” 文件夹下，并进行解压。解压之后会在该目录下生成“Images”文件夹。

  2.安装代码运行所需要的环境：

  ```python
  numpy
  pandas
  tensorflow-gpu==1.15.1
  matplotlib
  sklearn
  tqdm
  keras==2.3.1
  ```
  3.使用juputer note打开code.ipynb，依次运行每个单元格进行训练

  4.传入新的图片数据，调用相关函数进行预测

* 团队介绍：

  团队名称：Sunburst

  团队成员：赵现锋

  联系方式：17864211005

* 使用到的 AWS 技术：

  使用Amazon SageMaker提供的GPU对模型进行训练。

