import cv2
import os
import boto3
import json

def check_frame(frame):
	payload = json.dumps(frame.tolist())
	response = client.invoke_endpoint(EndpointName=ENDPOINT_NAME, ContentType='application/json',Body=payload)
	res = json.load(response['Body'])['predictions']
	return res[0] > res[1]

cap = cv2.VideoCapture('动画师如何用蔬菜水果拍摄一段定格动画，看饿了.flv') #打开摄像头
while True:
	ret, frame = cap.read() #读取摄像头画面
	cv2.imshow('v', frame)
	cv2.waitKey(30)
	# if not check_frame(frame): #判断是否有腐烂的水果
	# 	print('有腐烂的水果')
#初始化调用endpoint
ENDPOINT_NAME = 'sagemaker-tensorflow-serving-2020-09-14-21-13-59-342'
client = boto3.client('runtime.sagemaker', region_name='cn-northwest-1', aws_access_key_id='', aws_secret_access_key='')

