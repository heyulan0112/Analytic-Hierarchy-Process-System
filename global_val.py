# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 12:56:10 2021

@author: PC
"""

from tkinter import *
from tkinter.ttk import Treeview
from tkinter.ttk import Combobox
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename
from tkinter.simpledialog import *
import configparser
from PIL import Image, ImageTk

main_page = None
config = configparser.ConfigParser()
global config_file

#存储专家们对应的问卷的存储路径
experts = []
#存储专家的名字
experts_name = []
#False 问卷导入，True手工输入
human_load = False
#人工录入数据的时候存储各个矩阵的值
human_load_matrixs = {}

start_row = {}

def get_image(filename,width,height):
    image = Image.open(filename).resize((width,height))
    return ImageTk.PhotoImage(image)
