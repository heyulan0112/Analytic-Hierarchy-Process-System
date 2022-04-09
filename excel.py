# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 12:56:10 2021

@author: PC
"""

import xlwt
import xlrd
import numpy as np
from global_val import *

def create_excel(file_name,path):
    criterions = config.options('Criterion')
    len_cri = len(criterions)
    f = xlwt.Workbook()
    survey = f.add_sheet('Survey', cell_overwrite_ok = True)
    row = 0
    column = 0
    survey.write(row, column, config.get('Goal','goal'))
    if not config.has_section('Excel_row'):
        config.add_section('Excel_row')
    config['Excel_row'][config.get('Goal','goal')] = str(row)
    for c in range(len_cri):
        column += 1
        survey.write(row, column, criterions[c])
    for c in range(len_cri):
        row += 1
        survey.write(row, 0, criterions[c])
    for cri in criterions:
        row += 2
        column = 0
        survey.write(row, column, cri)
        config['Excel_row'][cri] = str(row)
        plans_str = config.get('Criterion', cri)
        plans = plans_str.split('&')
        for p in plans:
            column += 1
            survey.write(row, column, p)
        for p in plans:
            row += 1
            survey.write(row, 0, p)
    f.save('{}/{}.xls'.format(path,file_name))
    config.write(open(config.get('Path','path'), "w"))

def load_excel(file_name, mtr_name, n):
    data = xlrd.open_workbook(file_name)
    table = data.sheets()[0]
    row = 0
    a = np.zeros((n, n))
    row = start_row[mtr_name]
    row += 1
    for i in range(0, n):
        for j in range(i, n):
            if i == j:
                scale = 1
            else:
                scale = float(table.cell(i+row,j+1).value)
            a[i][j] = scale
            if scale == 0:
                a[j][i] = 0
            else:
                a[j][i] = float(1/scale)
    return a

def export_result(path, file_name):
    f = xlwt.Workbook()

    ignore_session = ['Criterion','Goal','Experts_Info','Excel_row','Path','Plan_link','Level']
    export_sessions = config.sections()
    for s in ignore_session:
        if s in export_sessions:
            export_sessions.remove(s)

    for ex_s in export_sessions:
        if ex_s == 'Plan':
            ranked_result = f.add_sheet('综合结果', cell_overwrite_ok = True)
        else:
            sheet_name = ex_s + '专家的结果'
            ranked_result = f.add_sheet(sheet_name, cell_overwrite_ok=True)
        row = 0
        ranked_result.write(row, 0, '方案')
        ranked_result.write(row,1,'权重')
        for alt in config.options(ex_s):
            row += 1
            ranked_result.write(row, 0, alt)
            weight_val = config.getfloat(ex_s, alt)
            weight_val = round(weight_val,4)
            ranked_result.write(row,1,str(weight_val))
    f.save('{}/{}.xls'.format(path, file_name))
