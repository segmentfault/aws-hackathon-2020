#! /usr/bin/env python
#  -*- coding: utf-8 -*-
import tkinter as tk
import result_support
from PIL import Image, ImageTk
import boto3
import json
import numpy as np


def vp_start_gui(path_):
    global val, w, root, imgPath_
    imgPath_ = path_
    root = tk.Tk()
    top = Toplevel1(root)
    result_support.init(root, top)
    root.mainloop()


w = None


def create_Toplevel1(rt, *args, **kwargs):
    global w, w_win, root
    root = rt
    w = tk.Toplevel(root)
    top = Toplevel1(w)
    result_support.init(w, top, *args, **kwargs)
    return (w, top)


def destroy_Toplevel1():
    global w
    w.destroy()
    w = None


class Toplevel1:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9'  # X11 color: 'gray85'
        _ana1color = '#d9d9d9'  # X11 color: 'gray85'
        _ana2color = '#ececec'  # Closest X11 color: 'gray92'
        font9 = "-family {Microsoft YaHei UI} -size 12"

        top.geometry("600x597+650+150")
        top.minsize(148, 1)
        top.maxsize(1924, 1056)
        top.resizable(1, 1)
        top.title("监测结果")
        top.configure(background="#d9d9d9")

        self.Label1 = tk.Label(top)
        self.Label1.place(relx=0.083, rely=0.089, height=405, width=495)
        self.Label1.configure(background="#d9d9d9")
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(text='''图像''')
        global _img0
        image1 = Image.open(imgPath_)
        _img0 = ImageTk.PhotoImage(image1, master=top)
        self.Label1.configure(image=_img0)

        self.Label2 = tk.Label(top)
        self.Label2.place(relx=0.033, rely=0.888, height=26, width=146)
        self.Label2.configure(background="#d9d9d9")
        self.Label2.configure(disabledforeground="#a3a3a3")
        self.Label2.configure(font=font9)
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(text='''监测结果是：''')

        self.Label3 = tk.Label(top)
        self.Label3.place(relx=0.267, rely=0.888, height=26, width=405)
        self.Label3.configure(anchor='w')
        self.Label3.configure(background="#d9d9d9")
        self.Label3.configure(disabledforeground="#a3a3a3")
        self.Label3.configure(foreground="#000000")
        self.Label3.configure(text='''请稍等~''')

        self.doAWSService(imgPath_)

    def doAWSService(self, file_name):
        runtime_client = boto3.client(service_name='runtime.sagemaker', region_name='cn-northwest-1',
                                      aws_access_key_id='AKIAQEVSSP223LKBUAXL',
                                      aws_secret_access_key='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', )

        with open(file_name, 'rb') as f:
            payload = f.read()
            payload = bytearray(payload)

        response = runtime_client.invoke_endpoint(EndpointName='zslendpoint',
                                                  ContentType='application/x-image',
                                                  Body=payload)
        result = response['Body'].read()
        result = json.loads(result)
        index = np.argmax(result)
        object_categories = ['其他垃圾', '厨余垃圾', '可回收物', '有害垃圾']

        self.Label3.configure(text="检测结果是 - " + object_categories[index] + ", 可能性 - " + str(result[index]))


if __name__ == '__main__':
    vp_start_gui('')
