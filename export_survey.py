# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 12:56:10 2021

@author: PC
"""

from global_val import *
from excel import *
import os.path

def select_path(path):
    path_str = askdirectory()
    path.set(path_str)

def export(path,file_name):
    try:
        if not os.path.exists(path) or file_name == '':
            raise ValueError('路径不存在')
        create_excel(file_name,path)
        messagebox.showinfo(title='提示', message='问卷生成成功')
    except:
        messagebox.showinfo(title='提示', message='问卷生成失败')

def survey():
    survey_page = Toplevel(main_page)
    survey_page.geometry('600x300')
    path = StringVar()
    lb_name = Label(survey_page,text='问卷名')
    lb_name.place(relx=0.1,rely=0.1)
    e_name = Entry(survey_page)
    e_name.place(relx=0.1,rely=0.2)
    lb_path = Label(survey_page,text='存储路径')
    lb_path.place(relx=0.1,rely=0.3)
    e_path = Entry(survey_page,textvariable = path)
    e_path.place(relx=0.1,rely=0.4)
    bt_select = Button(survey_page,text='选择',command = lambda: select_path(path=path))
    bt_select.place(relx=0.1,rely=0.5)
    bt_export = Button(survey_page,text='导出',command = lambda: export(path=e_path.get(),file_name=e_name.get()))
    bt_export.place(relx=0.2,rely=0.5)
    bt_quit = Button(survey_page,text='返回',command = lambda: survey_page.destroy())
    bt_quit.place(relx=0.3,rely=0.5)
    survey_page.mainloop()