# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 12:56:10 2021

@author: PC
"""

from model_operation import *
from export_survey import *
from data_load import *
from result_operation import *
from global_val import *
import os.path

def new_project(top_level_page,last_page,path,file_name):
    last_page.destroy()
    try:
        if not os.path.exists(path):
            raise ValueError('wrong path')
    except Exception as ex:
        messagebox.showinfo(title='提示', message='项目路径不存在')
    config_file = path + '/' + file_name + '.txt'
    file = open(config_file, 'w')
    file.close()
    config.read(config_file, encoding="utf-8")
    sections = ['Criterion', 'Plan', 'Goal', 'Experts_Info','Path','Plan_link','Level']
    for s in sections:
        if not config.has_section(s):
            config.add_section(s)
    config.set('Path','path',config_file)
    config.write(open(config_file, "w"))

    main_page = Toplevel(top_level_page)
    main_page.geometry('600x300')
    canvas = Canvas(main_page,width=600,height=300)
    pic = get_image('./图片/background.jpeg',600,300)
    canvas.create_image(300,150,image=pic)
    canvas.pack()

    menu = Menu(main_page)
    create_model = Menu(menu)
    create_survey = Menu(menu)
    load_data = Menu(menu)
    show_result = Menu(menu)

    create_model.add_command(label='编辑层次结构模型',command=model)
    create_survey.add_command(label='生成专家调查问卷',command=survey)
    load_data.add_command(label='导入问卷数据',command=load_survey)
    load_data.add_separator()
    load_data.add_command(label='手工输入数据',command=lambda :human_load_data(matrix_name=config.get('Goal','goal'),dim=
                                                                         len(config.options('Criterion')),related_index=
                                                                         config.options('Criterion')))
    show_result.add_command(label='查看决策结果',command=result)

    menu.add_cascade(label='新建',menu=create_model)
    menu.add_cascade(label='导出',menu=create_survey)
    menu.add_cascade(label='导入', menu=load_data)
    menu.add_cascade(label='查看',menu=show_result)

    main_page['menu'] = menu
    main_page.mainloop()

def create_project(last_page):
    project_page = Toplevel(last_page)
    project_page.geometry('600x300')
    canvas = Canvas(project_page,width=600,height=300)
    pic = get_image('./图片/background5.jpeg',600,300)
    canvas.create_image(300,150,image=pic)
    canvas.pack()

    path = StringVar()
    lb_name = Label(project_page,text='项目名')
    lb_name.place(relx=0.1,rely=0.1)
    e_name = Entry(project_page)
    e_name.place(relx=0.1,rely=0.2)
    lb_path = Label(project_page,text='项目路径')
    lb_path.place(relx=0.1,rely=0.35)
    e_path = Entry(project_page,textvariable = path)
    e_path.place(relx=0.1,rely=0.45)
    bt_select = Button(project_page,text='选择',highlightbackground="snow",command = lambda: select_path(path=path))
    bt_select.place(relx=0.1,rely=0.6)
    bt_export = Button(project_page,text='创建',highlightbackground="snow",command = lambda: new_project(top_level_page=last_page,last_page=project_page,path=e_path.get(),file_name=e_name.get()))
    bt_export.place(relx=0.2,rely=0.6)
    bt_quit = Button(project_page,text='返回',highlightbackground="snow",command = lambda: project_page.destroy())
    bt_quit.place(relx=0.3,rely=0.6)
    project_page.mainloop()

def open_project(top_level_page,last_page,path):
    last_page.destroy()
    try:
        if not os.path.exists(path):
            raise ValueError('wrong path')
    except Exception as ex:
        messagebox.showinfo(title='提示', message='项目不存在')
    config_file = path
    config.read(path, encoding="utf-8")
    sections = ['Criterion', 'Plan', 'Goal', 'Experts_Info','Path','Plan_link','Level']
    for s in sections:
        if not config.has_section(s):
            config.add_section(s)
    config.set('Path', 'path', path)
    config.write(open(path, "w"))
    if config.has_section('Excel_row'):
        for option in config.options('Excel_row'):
            start_row[option] = config.getint('Excel_row',option)

    ex_names = config.options('Experts_Info')
    for e in ex_names:
        experts_name.append(e)
        experts.append(config.get('Experts_Info',e))

    main_page = Toplevel(top_level_page)
    main_page.geometry('600x300')
    canvas = Canvas(main_page,width=600,height=300)
    pic = get_image('./图片/background.jpeg',600,300)
    canvas.create_image(300,150,image=pic)
    canvas.pack()

    menu = Menu(main_page)
    create_model = Menu(menu)
    create_survey = Menu(menu)
    load_data = Menu(menu)
    show_result = Menu(menu)

    create_model.add_command(label='编辑层次结构模型',command=model)
    create_survey.add_command(label='生成专家调查问卷',command=survey)
    load_data.add_command(label='导入问卷数据',command=load_survey)
    load_data.add_separator()
    load_data.add_command(label='手工输入数据',command=lambda :human_load_data(matrix_name=config.get('Goal','goal'),dim=
                                                                         len(config.options('Criterion')),related_index=
                                                                         config.options('Criterion')))
    show_result.add_command(label='查看决策结果',command=result)

    menu.add_cascade(label='新建',menu=create_model)
    menu.add_cascade(label='导出',menu=create_survey)
    menu.add_cascade(label='导入', menu=load_data)
    menu.add_cascade(label='查看',menu=show_result)

    main_page['menu'] = menu
    main_page.mainloop()

def select_project(last_page):
    project_page = Toplevel(last_page)
    project_page.geometry('600x300')
    canvas = Canvas(project_page,width=600,height=300)
    pic = get_image('./图片/background5.jpeg',600,300)
    canvas.create_image(300,150,image=pic)
    canvas.pack()

    path = StringVar()
    lb_path = Label(project_page,text='打开项目')
    lb_path.place(relx=0.1,rely=0.1)
    e_path = Entry(project_page,textvariable = path)
    e_path.place(relx=0.1,rely=0.2)
    bt_select = Button(project_page,text='选择',highlightbackground="snow",command = lambda: fetch_path(path=path))
    bt_select.place(relx=0.1,rely=0.35)
    bt_export = Button(project_page,text='打开',highlightbackground="snow",command = lambda: open_project(top_level_page=last_page,last_page=project_page,path=e_path.get()))
    bt_export.place(relx=0.2,rely=0.35)
    bt_quit = Button(project_page,text='返回',highlightbackground="snow",command = lambda: project_page.destroy())
    bt_quit.place(relx=0.3,rely=0.35)
    project_page.mainloop()

if __name__ == '__main__':
    start_page = Tk()
    start_page.geometry('600x300')
    canvas = Canvas(start_page,width=600,height=300)
    pic = get_image('./图片/background.jpeg',600,300)
    canvas.create_image(300,150,image=pic)
    canvas.pack()

    bt_new = Button(start_page,text='新建项目',highlightbackground="white",command=lambda: create_project(last_page=start_page))
    bt_new.place(relx=0.1,rely=0.2)
    bt_open = Button(start_page,text='打开项目',highlightbackground="white",command=lambda: select_project(last_page=start_page))
    bt_open.place(relx=0.1,rely=0.4)
    bt_quit = Button(start_page,text='退出',highlightbackground="white",command= lambda :start_page.destroy())
    bt_quit.place(relx=0.1,rely=0.6)
    start_page.mainloop()
