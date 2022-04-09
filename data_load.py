# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 12:56:10 2021

@author: PC
"""

from global_val import *
from ahp import *
import os.path

def fetch_path(path):
    path_str = askopenfilename()
    path.set(path_str)

def survey_import(path,box,cmb_level,ex_name):
    try:
        if not os.path.exists(path) or ex_name == '':
            raise ValueError('error')
        if len(start_row.keys()) == 0:
            raise Exception('error')
        ahp(ex_name,path)
        level_text = cmb_level.get()
        level = 0
        if level_text == '非常重要':
            level = 5
        elif level_text == '重要':
            level = 4
        elif level_text == '普通':
            level = 3
        elif level_text == '一般':
            level = 2
        elif level_text == '不重要':
            level = 1
        config.set('Level', ex_name, str(level))
        config.write(open(config.get('Path', 'path'), "w"))
        experts.append(path)
        experts_name.append(ex_name)
        messagebox.showinfo(title='提示', message='问卷导入成功')
        config['Experts_Info'][ex_name] = path
        config.write(open(config.get('Path','path'), "w"))
        box.insert(END,ex_name)
    except Exception as ex:
        messagebox.showinfo(title='提示', message='导入失败,建议检查问卷格式')

def delete_selected_expert(event):
    object = event.widget
    index = object.curselection()
    expert_name = object.get(index)
    expert_sur_path = config.get('Experts_Info',expert_name)
    experts.remove(expert_sur_path)
    experts_name.remove(expert_name)
    config.remove_option('Experts_Info',expert_name)
    config.remove_option('Level',expert_name)
    config.remove_section(expert_name)
    config.write(open(config.get('Path', 'path'), "w"))
    object.delete(index)

def load_survey():
    human_load = False
    ld_sur_page = Toplevel(main_page)
    ld_sur_page.geometry('600x300')
    path = StringVar()
    lb_name = Label(ld_sur_page,text='专家名')
    lb_name.place(relx=0.1,rely=0.1)
    e_name = Entry(ld_sur_page,width=10,)
    e_name.place(relx=0.1,rely=0.2)
    lb_level = Label(ld_sur_page,text='专家级别')
    lb_level.place(relx=0.1,rely=0.6)

    cmb_level = Combobox(ld_sur_page)
    cmb_level.place(relx=0.1,rely=0.7)
    cmb_level['value'] = ('非常重要','重要','普通','一般','不重要')
    cmb_level.current(2)

    lb_path = Label(ld_sur_page,text='需导入的问卷路径')
    lb_path.place(relx=0.1,rely=0.3)
    e_path = Entry(ld_sur_page,textvariable = path)
    e_path.place(relx=0.1,rely=0.4)
    bt_fetch = Button(ld_sur_page,text='选择',command = lambda: fetch_path(path=path))
    bt_fetch.place(relx=0.1,rely=0.5)
    list_import = Listbox(ld_sur_page)
    list_import.place(relx=0.5,rely=0.2)

    list_import.bind('<Double-1>',delete_selected_expert)
    bt_import = Button(ld_sur_page,text='导入',command = lambda: survey_import(path=e_path.get(),box=list_import,
                                                                             cmb_level=cmb_level,ex_name=e_name.get()))
    bt_import.place(relx=0.2,rely=0.5)
    bt_quit = Button(ld_sur_page,text='返回',command = lambda: ld_sur_page.destroy())
    bt_quit.place(relx=0.3,rely=0.5)
    lb_import = Label(ld_sur_page,text='已导入的专家')
    lb_import.place(relx=0.5,rely=0.1)

    for existed_expert in experts_name:
        list_import.insert(END,existed_expert)
        expert_sur_path = config.get('Experts_Info', existed_expert)
        if not expert_sur_path in experts:
            experts.append(expert_sur_path)
        if not existed_expert in experts_name:
            experts_name.append(existed_expert)
    ld_sur_page.mainloop()

def switch_next_matrix(current_page,current_matrix):
    current_page.destroy()
    criterions = config.options('Criterion')
    next_matrix = ''
    if current_matrix == config.get('Goal','goal'):
        next_matrix = criterions[0]
        plans = config.get('Criterion', next_matrix)
        plans = plans.split('&')
        human_load_data(next_matrix,len(plans),plans)
    else:
        index = criterions.index(current_matrix)
        if index != (len(criterions)-1):
            next_matrix = criterions[index + 1]
            plans = config.get('Criterion',next_matrix)
            plans = plans.split('&')
            human_load_data(next_matrix, len(plans), plans)

def temp_save_list(val,entry_name):
    dot_index = entry_name.rindex('.')
    name = entry_name[dot_index+1:]
    index = int(name)
    if index < len(data):
        data[index] = val
    else:
        data.append(val)
    return True

def load_to_matrix(name,dim):
    a = np.zeros((dim, dim))
    index = 0
    for i in range(0,dim):
        for j in range(i,dim):
            if i == j:
                scale = 1
            else:
                scale = float(data[index])
                index += 1
            a[i][j] = scale
            if scale == 0 or scale == 0.0:
                a[j][i] = 0
            else:
                a[j][i] = 1 / scale
    human_load_matrixs[name] = a

    goal = config.get('Goal','goal')
    if name != goal:
        criterions = config.options('Criterion')
        index = criterions.index(name)
        if index == (len(criterions) - 1):
            human_load_ahp()

def human_load_data(matrix_name,dim,related_index):
    human_load = True
    i_page = Toplevel(main_page)
    i_page.tk_focusFollowsMouse()
    winWidth = 600
    winHeight = 300
    screenWidth = i_page.winfo_screenwidth()
    screenHeight = i_page.winfo_screenheight()

    x = int((screenWidth - winWidth) / 2)
    y = int((screenHeight - winHeight) / 2)

    i_page.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))
    i_page.resizable(0, 0)

    scroll_bar = Scrollbar(i_page)
    scroll_bar.pack(side=RIGHT, fill=Y)

    row_no = 55
    column_no1 = 10
    column_no2 = column_no1 + 100
    column_no3 = column_no2 + 100
    column_no4 = column_no3 + 100

    bt_next_matrix = Button(i_page,text='下一页',command=lambda:switch_next_matrix(current_page= i_page, current_matrix=matrix_name))
    bt_next_matrix.place(x=column_no2,y=row_no)

    text = matrix_name + '的判断矩阵'
    lb_name = Label(i_page,text=text)
    lb_name.place(x=column_no1,y=row_no)

    global data
    data = []
    global active_entry_name

    temp_save = i_page.register(temp_save_list)
    num = 0
    for i in range(dim):
        for j in range(i+1,dim):
            row_no = row_no + 50
            num += 1
            lb_a = Label(i_page,text=related_index[i])
            lb_a.place(x=column_no1,y=row_no)
            lb_compare = Label(i_page,text='compare')
            lb_compare.place(x=column_no2,y=row_no)
            lb_b = Label(i_page,text=related_index[j])
            lb_b.place(x=column_no3,y=row_no)
            global entry_i
            val = DoubleVar()
            name = num - 1
            entry_i = Entry(i_page,name=str(name),width=5,textvariable=val,validate='focusout',validatecommand= (temp_save, '%P','%W'))
            entry_i.place(x=column_no4,y=row_no)

    bt_finish = Button(i_page, text='完成输入', command=lambda: load_to_matrix(name=matrix_name, dim=dim))
    bt_finish.place(x=column_no1,y=5)
    i_page.mainloop()
