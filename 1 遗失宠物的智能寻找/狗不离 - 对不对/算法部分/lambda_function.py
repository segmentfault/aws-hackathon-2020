import json
import os
import io
import boto3
import json
import csv
ENDPOINT_NAME = 'sagemaker-tensorflow-serving-2020-09-07-21-13-59-342'
client = boto3.client('runtime.sagemaker', region_name='cn-northwest-1')
def lambda_handler(event, context):
    payload = event['img']
    response = client.invoke_endpoint(EndpointName=ENDPOINT_NAME, ContentType='application/json',Body=payload)
    print(response['Body'])
    return {
        'statusCode': 200,
        'body': json.load(response['Body'])
    }
