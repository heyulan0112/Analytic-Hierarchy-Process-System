# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 12:56:10 2021

@author: PC
"""

from global_val import *

def add_goal(goal):
    try:
        config.set('Goal','goal',goal)
        tree.insert('',0,goal,text=goal,tag='goal')
        config.write(open(config.get('Path','path'), "w"))
    except Exception as ex:
        messagebox.showinfo(title='提示', message='添加失败')

def add_criterion(cri):
    try:
        if tree.tag_has(cri):
            raise ValueError('error')
        goal = config.get('Goal','goal')
        tree.insert(goal,'end',cri, text=cri,tag=cri)
    except Exception as ex:
        messagebox.showinfo(title='提示', message='添加失败')

def add_alternative(cri,alt):
    try:
        if cri == '' or alt == '' or tree.tag_has(cri+alt):
            raise ValueError("指标或方案名缺省")
        tree.insert(cri, 'end', text=alt, tag=cri + alt)
        if config.has_option('Criterion',cri):
            val_str = config.get('Criterion',cri)
            val_str = val_str + '&' + alt
            config.set('Criterion',cri,val_str)
        else:
            config.set('Criterion',cri,alt)
        config.set('Plan',alt,'0')
        num_link = 0
        if config.has_option('Plan_link',alt):
            num_link = config.getint('Plan_link',alt)
        config.set('Plan_link',alt, str(num_link+1))
        config.write(open(config.get('Path','path'), "w"))
    except Exception as ex:
        messagebox.showinfo(title='提示', message='添加失败')
        print(ex)

def delete_selected_item(event):
    item = tree.selection()
    goal = config.get('Goal','goal')
    criterions = config.options('Criterion')
    text = tree.item(item, 'text')
    try:
        if text == goal:
            raise ValueError('error')
    except Exception as ex:
        messagebox.showinfo(title='提示', message='不支持删除决策目标')

    if text in criterions:
        config.remove_option('Criterion',text)
        if config.has_option('Excel_row',text):
            config.remove_option('Excel_row',text)

    else:
        num = config.getint('Plan_link',text)
        if num-1 == 0:
            config.remove_option('Plan',text)
        config.set('Plan_link',text,str(num-1))
        parent = tree.parent(item)
        plans = config.get('Criterion',tree.item(parent,'text'))
        plans = plans.split('&')
        plans.remove(text)
        plans = '&'.join(plans)
        config.set('Criterion',tree.item(parent,'text'),plans)
    tree.delete(item)
    config.write(open(config.get('Path','path'), "w"))

def fetch_selected_item(event):
    item = tree.selection()
    var.set(tree.item(item, 'text'))

def model():
    model_page = Toplevel(main_page)
    model_page.geometry('600x300')

    e_goal = Entry(model_page,width=10)
    e_cri = Entry(model_page,width=10)
    e_alt = Entry(model_page,width=10)
    global var
    var = StringVar()
    e_alt_link = Entry(model_page,width=10,textvariable=var)
    e_goal.place(relx=0.2,rely=0.2)
    e_cri.place(relx=0.2, rely=0.4)
    e_alt.place(relx=0.2, rely=0.6)
    e_alt_link.place(relx=0.2, rely=0.7)

    lb_goal = Label(model_page,text='决策目标')
    lb_goal.place(relx=0.1,rely=0.2)
    lb_cri = Label(model_page,text='指标名')
    lb_cri.place(relx=0.1,rely=0.4)
    lb_alt = Label(model_page,text='方案名')
    lb_alt.place(relx=0.1,rely=0.6)

    lb_alt_link = Label(model_page,text='关联指标')
    lb_alt_link.place(relx=0.1,rely=0.7)

    bt_add_goal = Button(model_page, text='+  添加决策目标',command=lambda :add_goal(goal=e_goal.get()))
    bt_add_criterion = Button(model_page, text='+  添加指标因素',command=lambda :add_criterion(cri=e_cri.get()))
    bt_add_alternative = Button(model_page, text='+  添加决策方案',command=lambda :add_alternative(cri=e_alt_link.get(),
                                                                                             alt=e_alt.get()))
    bt_add_goal.place(relx=0.1, rely=0.1)
    bt_add_criterion.place(relx=0.1, rely=0.3)
    bt_add_alternative.place(relx=0.1, rely=0.5)
    bt_quit = Button(model_page, text='-  完成', command=lambda: model_page.destroy())
    bt_quit.place(relx=0.1,rely=0.8)

    global tree
    tree= Treeview(model_page, show="tree")
    tree.place(relx=0.5,rely=0.1)
    x = tree.get_children()
    for item in x:
        tree.delete(item)
    tree.bind('<Double-1>', fetch_selected_item)
    tree.bind('<KeyPress-BackSpace>', delete_selected_item)

    if config.has_option('Goal','goal'):
        goal = config.get('Goal','goal')
        tree.insert('', 0, goal, text=goal, values=('1'), tag='goal')
        cris = config.options('Criterion')
        for c in cris:
            tree.insert(goal, 'end', c, text=c, tag=c)
            alts = config.get('Criterion',c)
            alts = alts.split('&')
            for a in alts:
                tree.insert(c, 'end', text=a, tag=a)
    model_page.mainloop()
