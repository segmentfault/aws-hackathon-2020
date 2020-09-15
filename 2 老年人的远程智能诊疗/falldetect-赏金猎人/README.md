# 跌倒检测
本项目使用 OpenVINO toolkit 的人体姿势预训练模型 [human-pose-estimation-0001](https://docs.openvinotoolkit.org/latest/_models_intel_human_pose_estimation_0001_description_human_pose_estimation_0001.html) 进行跌倒检测

# 检测原理
- 使用 opencv 从摄像头、视频文件读取每一帧视频，并判断 头、颈部、肩膀的位置
- 对比每一帧视频，当发现位置为水平时判定为跌倒
- 将判定跌倒的视频帧标注，并显示或输出为视频

# 使用 docker 编译镜像
```
docker build -t falldetect .
docker run -it --rm -v "$PWD:/app" falldetect
```

# 运行
```
# 首先初始化环境
cd /opt/intel/openvino
source bin/setupvars.sh

# 确认环境变量已经设置了 openvino 路径
echo $PYTHONPATH 

# 执行代码
cd /app
python3 fall_detection.py -i example/demo.mp4 
```