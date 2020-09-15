FROM openvino/ubuntu18_dev:2020.1
USER root
ADD sources.list /etc/apt




RUN pip3 install  -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip
RUN pip3 install  -i https://pypi.tuna.tsinghua.edu.cn/simple numpy exitstatus opencv-python

RUN apt update && apt install -y libsm6 libxext6 sudo libpython3.6

RUN mkdir /app
VOLUME /app

CMD ["/bin/bash"]