# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 12:56:10 2021

@author: PC
"""

from global_val import *
from ahp import *
from export_survey import select_path

def clear_tree():
    x=tree_weight.get_children()
    for item in x:
        tree_weight.delete(item)

def fetch_ex_result(event):
    clear_tree()
    object = event.widget
    index = object.curselection()
    name = object.get(index)
    weight_result = {}
    list = []
    if name == '综合结果':
        if len(experts_name) != 0:
            group_decision()
        alternatives = config.options('Plan')
        for index in range(len(alternatives)):
            value = round(config.getfloat('Plan', alternatives[index]),4)
            weight_result[alternatives[index]] = value
    else:
        alternatives = config.options(name)
        for index in range(len(alternatives)):
            value = round(config.getfloat(name, alternatives[index]),4)
            weight_result[alternatives[index]] = value

    sorted_weight = sorted(zip(weight_result.values(), weight_result.keys()), reverse=True)
    for w in sorted_weight:
        dict_result = {}
        dict_result['alternative'] = w[1]
        dict_result['weight'] = w[0]
        list.append(dict_result)
    i = 0
    for v in list:
        tree_weight.insert('', i, values=(v.get('alternative'), v.get('weight')))
        i += 1

def execute_result_export(file_name,path):
    export_result(path,file_name)
    messagebox.showinfo(title='提示', message='文件导出成功')

def export_weight_result(master_page):
    export_page = Toplevel(master_page)
    export_page.geometry('600x300')
    path = StringVar()
    lb_name = Label(export_page,text='文件名')
    lb_name.place(relx=0.1,rely=0.1)
    e_name = Entry(export_page)
    e_name.place(relx=0.1,rely=0.2)
    lb_path = Label(export_page,text='存储路径')
    lb_path.place(relx=0.1, rely=0.3)
    e_path = Entry(export_page, textvariable=path)
    e_path.place(relx=0.1, rely=0.4)
    bt_select = Button(export_page, text='选择', command=lambda: select_path(path=path))
    bt_select.place(relx=0.1, rely=0.5)
    bt_export = Button(export_page, text='导出', command=lambda: execute_result_export(path=e_path.get(),file_name=e_name.get()))
    bt_export.place(relx=0.2, rely=0.5)
    bt_quit = Button(export_page, text='返回', command=lambda: export_page.destroy())
    bt_quit.place(relx=0.3, rely=0.5)
    export_page.mainloop()

def result():
    show_page = Toplevel(main_page)
    show_page.geometry('800x300')

    columns = ('alternative', 'weight')
    global tree_weight
    tree_weight = Treeview(show_page,show = 'headings', columns = columns, selectmode = BROWSE)
    tree_weight.place(relx=0.4,rely=0.1)

    tree_weight.column('alternative', anchor='center')
    tree_weight.column('weight', anchor='center')
    tree_weight.heading('alternative', text='方案')
    tree_weight.heading('weight', text='权重')

    list_experts = Listbox(show_page)
    list_experts.place(relx=0.1, rely=0.1)
    list_experts.insert(END, '综合结果')
    for name in experts_name:
        list_experts.insert(END,name)
    list_experts.bind('<<ListboxSelect>>', fetch_ex_result)

    bt_export = Button(show_page,text='导出Excel',command=lambda: export_weight_result(master_page=show_page))
    bt_export.place(relx=0.1,rely= 0.7)
    bt_finish = Button(show_page,text='返回',command= lambda :show_page.destroy())
    bt_finish.place(relx=0.25,rely=0.7)
    show_page.mainloop()
