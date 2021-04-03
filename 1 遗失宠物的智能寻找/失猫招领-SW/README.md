<img src="https://fzhcats.s3-ap-northeast-1.amazonaws.com/documents/cat.png" width="100">

----------

# 🐱失猫招领-[主页](http://lostandfound-env.eba-ftezekhq.ap-northeast-1.elasticbeanstalk.com/)


基于宠物猫分类智能识别的遗失宠物猫信息发布共享平台  

家养宠物猫意外走失心急如焚？发现疑似迷路的宠物猫却不知如何找到它的主人？不要着急，将猫的照片发布到[**失猫招领**](http://lostandfound-env.eba-ftezekhq.ap-northeast-1.elasticbeanstalk.com/)，我们将利用深度学习模型智能识别猫的品种、颜色等外貌特征，并综合考虑您的所在地区，猫的年龄，发布时间等因素，向您推荐最相似的宠物猫信息，帮您尽快找到您丢失的宠物猫或走失宠物猫的主人。


----------


## 功能特性


**已实现：**
1. 邮箱注册登录
2. 上传猫的图片并填写基本信息，发布丢失猫或发现猫的启事
3. 根据上传的猫照片识别出猫的分类，并综合所得信息推荐所有相似的猫的启事
4. 用户也可以自己根据发布位置，猫的分类，启事分类（Lost还是Found）以及发布时间段等条件手动筛选平台上的所有启事
5. 用户可在个人主页查看并删除自己已发布的启事

**TODO:**
1. 获取更大更好的数据集重新训练模型，并尝试使用AWS segemaker或AWS lambda部署预测服务
2. 邮件通知功能，定期向丢失猫的用户发送与Ta丢失的猫相似的被路人发现走失的猫的启事
2. 上传音频功能，用户可以在启事中上传猫的叫声录音，通过声纹识别寻找相似的猫，进一步缩小寻找范围
3. 完善界面


----------
## 作品截图



1. 注册


<img src="https://fzhcats.s3-ap-northeast-1.amazonaws.com/documents/signup.jpg" width = 400>


2. 登录


<img src="https://fzhcats.s3-ap-northeast-1.amazonaws.com/documents/signin.jpg" width = 400>


3. 首页


<img src="https://fzhcats.s3-ap-northeast-1.amazonaws.com/documents/homepage.jpg" width = 400>


4. 发布启事，其中品种（种类）一栏将根据用户上传的猫的照片自动填充模型智能识别的结果


<img src="https://fzhcats.s3-ap-northeast-1.amazonaws.com/documents/lostBS.jpg" width = 400>


5. 若智能识别猫的种类结果错误，也可手动重新输入


<img src="https://fzhcats.s3-ap-northeast-1.amazonaws.com/documents/hint.jpg" width = 400>


6. 发布成功后，智能匹配相似的猫


<img src="https://fzhcats.s3-ap-northeast-1.amazonaws.com/documents/recom.jpg" width = 400>


7. 个人主页可查看已发布的启事，并可以删除自己发布的启事


<img src="https://fzhcats.s3-ap-northeast-1.amazonaws.com/documents/my.jpg" width = 400>
<img src="https://fzhcats.s3-ap-northeast-1.amazonaws.com/documents/myposts.jpg" width = 400>
<img src="https://fzhcats.s3-ap-northeast-1.amazonaws.com/documents/deletemine.jpg" width = 400>


8. 首页可以按条件过滤查询


<img src="https://fzhcats.s3-ap-northeast-1.amazonaws.com/documents/filter.jpg" width = 400>
<img src="https://fzhcats.s3-ap-northeast-1.amazonaws.com/documents/filterresult.jpg" width = 400>



----------
## 使用的AWS服务和技术


1. AWS EC2：作为存放web服务的容器
2. AWS Elastic Beanstalk：创建tomcat容器和Java环境，并一键部署web应用
3. AWS RDS：创建并使用MySQL数据库
4. AWS SegeMaker：深度学习模型训练和保存
5. AWS S3：对象存储，存储训练数据集和模型，Elastic Beanstalk需要使用的配置文件和历史版本，以及作为图床存储用户上传的图片
6. AWS IAM：资源访问权限管理


----------
## 架构设计


<img src="https://fzhcats.s3-ap-northeast-1.amazonaws.com/documents/architecture.png" >


### 1. 数据集获取和模型训练


**数据集**  


我们利用必应图片搜集了中国最常见的宠物猫图片，分为13类并用数字表示：  
美国短毛猫-0，黑猫-1，英国短毛猫-2，奶牛猫（黑白猫）-3，折耳猫-4，加菲猫-5，橘猫-6，布偶猫-7，暹罗猫-8，斯芬克斯猫-9，狸花猫-10，三花猫（三色猫）-11，白猫 -12 
其中按颜色区分的分类（如白猫，黑猫，三花，橘猫等）主要是针对毛色繁多的非纯种猫和中华田园猫，而纯种猫的特征相对明显且毛色单一，因此不做颜色区分。  
经过人工筛选后，每种猫有200张图片，因此最终数据集大小是2600张图片。


**训练模型**


在AWS SegeMaker上创建Jupyter实例用于训练模型，代码见[/segemaker_jupyter](https://github.com/zerofang/aws-hackathon-2020/blob/master/1%20%E9%81%97%E5%A4%B1%E5%AE%A0%E7%89%A9%E7%9A%84%E6%99%BA%E8%83%BD%E5%AF%BB%E6%89%BE/%E5%A4%B1%E7%8C%AB%E6%8B%9B%E9%A2%86-SW/segemaker_jupyter/train.ipynb)。  
由于我们能得到的数据量很小，也没有大量计算资源，直接利用现有数据集和计算资源直接训练模型的效果不佳，所以我们选择使用预训练的VGG16进行迁移学习，Keras使得这一实现非常容易，最终我们的模型结构如下：

<img src="https://fzhcats.s3-ap-northeast-1.amazonaws.com/documents/model_summary.png" >


经过训练和参数调优后，最终我们的模型的预测准确率达到80.27%，考虑到我们的数据集很小且筛选比较粗糙，这是个不错的结果。


<img src="https://fzhcats.s3-ap-northeast-1.amazonaws.com/documents/learning_curve.png" >


### 2. 用于预测猫的分类的Web API
我们将训练好的模型保存为saved model形式，并存放在AWS S3上，供用于预测猫的分类的Web API下载和使用。由于图片在输入到我们的模型之前需要进行裁剪，像素转换，归一化等预处理操作，而时间紧迫，我们此前没有使用Java做图像预处理的经验，所以我们这次没有选择使用AWS Lambda等工具部署模型。  


我们用flask做了一个微型Web API，见[predict_webapi](https://github.com/zerofang/aws-hackathon-2020/blob/master/1%20%E9%81%97%E5%A4%B1%E5%AE%A0%E7%89%A9%E7%9A%84%E6%99%BA%E8%83%BD%E5%AF%BB%E6%89%BE/%E5%A4%B1%E7%8C%AB%E6%8B%9B%E9%A2%86-SW/predict_webapi/predict.py)。我们创建了一个EC2实例，安装了Python3.7 + Tensorflow2.30运行环境，用于运行这个Web API服务。这一解决方案很粗糙，而且免费的EC2实例仅包含一个单核CPU计算资源，所以该API响应速度较慢，单次请求响应时间达到了数百毫秒，这是未来的优化点之一，未来我们将尝试使用AWS Lambda重新部署模型。


### 3.Web应用（网站主体）


**数据库表设计**  


以下是ER图和数据库表的字段及其描述（其中voice表已设计但未实现）：


<img src="https://fzhcats.s3-ap-northeast-1.amazonaws.com/documents/database.png" > 


user（用户表）
|  键   | 类型  | 描述 |
|  ----  | ----  | ---- |
| user_id  | BIGINT | 用户id |
| email  | VARCHAR(128) | 注册邮箱 |
| password | VARCHAR(32) | 密码 |


post（启事表）
|  键   | 类型  | 描述 |
|  ----  | ----  | ---- |
| post_id  | BIGINT | 启事id |
| user_id  | BIGINT | 关联user表的user_id |
| location | VARCHAR(10) | 字符串，6位地区码 |
| title | VARCHAR(128) | 启事标题 |
| description | VARCHAR(512) | 启事正文内容 |
| cat_class | TINYINT(1) | 数字，0到12，分别代表上面提到的13种猫 |
| type | TINYINT(1) | 启事类型，lost-0,found-1 |
| timestamp | BIGINT | 启事发表或更新的时间，毫秒数表示 |
| status | TINYINT(1) | 是否活跃，仍在寻找猫或寻找主人-0,已经找到或放弃寻找-1 |
| lof_time | BIGINT | 丢失或发现猫的时间 |
| cover_path | VATCHAR(256) | 启事封面照片路径 |
| email_notify | TINYINT(1) | 是否愿意接收邮箱通知 |
| adult | TINYINT(1) | 猫是否成年 |


photo（用户上传的猫的图片表）
|  键   | 类型  | 描述 |
|  ----  | ----  | ---- |
| photo_id | BIGINT | 图片id |
| post_id | BIGINT | 关联post表的post_id |
| path | VARCHAR(256) | 图片路径 |
| photo_index | TINYINT(1) | 图片顺序，=1时是封面 |
| cat_class | TINYINT(1) | 图片中猫的种类，0-12的数字表示 |


我们的数据库使用了基于AWS RDS的MySQL8.0版本数据库，创建数据库和表的SQL文件见[/lostandfound/cat.sql](https://github.com/zerofang/aws-hackathon-2020/blob/master/1%20%E9%81%97%E5%A4%B1%E5%AE%A0%E7%89%A9%E7%9A%84%E6%99%BA%E8%83%BD%E5%AF%BB%E6%89%BE/%E5%A4%B1%E7%8C%AB%E6%8B%9B%E9%A2%86-SW/lostandfound/cat.sql)


**Web前端、后端以及部署**


我们的web前端采用vue2.0开发，后端采用spring boot + ibatis开发，最终将前端静态页面与后端代码合并编译打包，使用AWS Elastic Beanstalk部署上线，线上运行容器环境是Tomcat8.5 + Java8。


值得一提的是从用户上传图片到获取预测结果的流程：当用户上传图片后，前端将图片上传到AWS S3，然后把图片的键（path）发送给用于预测分类的Web API，然后该API使用boto3从S3上按前端提供的键获取到图片，对图片进行预处理，输入到模型，将预测结果返回给前端，最后前端填充图片的cat_class字段，并将图片的完整信息发送给后端存档。


----------
## 编译部署指南


**1. 用于预测分类的flask Web API的部署**

首先从S3服务器上下载好saved_model，并上传到EC2服务器上，然后在EC2服务器上安装python3.7和pip，进入目录/predict_webapi，执行以下命令安装所需package：

    pip install -r requirements.txt

填充predict.py中用于身份认证的access_key等内容，然后在EC2服务器上不挂起启动：

    nohup python predict.py > predict.log 2>&1 &


**2. 前端VUE App编译**


进入目录/cat_lostandfound_front_end，编辑/cat_lostandfound_front_end/public/index.html，填写正确的IdentityPoolId和albumBucketName，保存，然后打开node.js，执行以下命令安装依赖和编译：

    npm i
    npm run build
    
编译完成后，将生成的所有静态文件复制粘贴到/lostandfound/src/main/resources/static目录下。


**3. Web应用的部署**

首先利用AWS RDS创建一个MySQL 8.0版本的数据库，执行sql脚本[/lostandfound/cat.sql]，然后填充/lostandfound/src/main/resources/application.properties中的数据库地址和用户名、密码等信息，在根目录下运行以生成war包：

    mvn clean package

找到target文件夹下的lostandfound-0.0.1-SNAPSHOT.war，打开AWS Elastic beanstalk，创建一个tomcat8.5+Java8环境，然后点击按钮上传部署即可，若部署完成后状态为绿色良好，则表示部署成功。


----------
## 贡献者名单及联系方式


[@zerofang](https://github.com/zerofang)(fangzihan@bupt.edu.cn)：🤔项目设计，💻编程（深度学习模型+Java后端），📃文档编写  


[@iamplex](https://github.com/iamplex)(panjing.binary@gmail.com)：💻编程（前端）
