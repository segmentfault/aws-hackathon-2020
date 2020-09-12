#! /usr/bin/env python
#  -*- coding: utf-8 -*-

import sys
from tkinter.filedialog import askopenfilename
import resultUI


def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top


# 使用aws服务
def select_file():
    path_ = askopenfilename()
    print(path_)
    sys.stdout.flush()
    if path_:
        resultUI.vp_start_gui(path_)


def destroy_window():
    global top_level
    top_level.destroy()
    top_level = None


if __name__ == '__main__':
    import mainUI

    mainUI.vp_start_gui()
