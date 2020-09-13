#! /usr/bin/env python
#  -*- coding: utf-8 -*-

import os.path
import sys
import tkinter as tk
from PIL import Image, ImageTk

import main_support


def vp_start_gui():
    global val, w, root
    global prog_location
    prog_call = sys.argv[0]
    prog_location = os.path.split(prog_call)[0]
    root = tk.Tk()
    top = Toplevel1(root)
    main_support.init(root, top)
    root.mainloop()


w = None


def create_Toplevel1(rt, *args, **kwargs):
    global w, w_win, root
    global prog_location
    prog_call = sys.argv[0]
    prog_location = os.path.split(prog_call)[0]
    # rt = root
    root = rt
    w = tk.Toplevel(root)
    top = Toplevel1(w)
    main_support.init(w, top, *args, **kwargs)
    return (w, top)


def destroy_Toplevel1():
    global w
    w.destroy()
    w = None


class Toplevel1:
    def __init__(self, top=None):
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9'  # X11 color: 'gray85'
        _ana1color = '#d9d9d9'  # X11 color: 'gray85'
        _ana2color = '#ececec'  # Closest X11 color: 'gray92'
        font9 = "-family {Microsoft YaHei UI} -size 12"

        top.geometry("982x516+596+191")
        top.minsize(148, 1)
        top.maxsize(1924, 1056)
        top.resizable(1, 1)
        top.title("城市垃圾污染监测系统")
        top.configure(background="#d9d9d9")

        self.Label1 = tk.Label(top)
        self.Label1.place(relx=0.102, rely=0.048, height=238, width=747)
        self.Label1.configure(background="#d9d9d9")
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(foreground="#000000")
        global _img0
        image1 = Image.open('/Volumes/Data/PyCharmProject/client/images/bg.jpeg')
        _img0 = ImageTk.PhotoImage(image1)
        self.Label1.configure(image=_img0)
        self.Label1.configure(text='''Label''')

        self.Label2 = tk.Label(top)
        self.Label2.place(relx=0.285, rely=0.678, height=30, width=150)
        self.Label2.configure(background="#d9d9d9")
        self.Label2.configure(disabledforeground="#a3a3a3")
        self.Label2.configure(font=font9)
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(text='''请选择文件：''')

        self.Button1 = tk.Button(top)
        self.Button1.place(relx=0.509, rely=0.601, height=123, width=121)
        self.Button1.configure(activebackground="#ececec")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(command=main_support.select_file)
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        global _img1
        image2 = Image.open('/Volumes/Data/PyCharmProject/client/images/upload.png')
        _img1 = ImageTk.PhotoImage(image2)
        self.Button1.configure(image=_img1)
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''Button''')


if __name__ == '__main__':
    vp_start_gui()
