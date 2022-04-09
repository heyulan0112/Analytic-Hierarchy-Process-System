# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 12:56:10 2021

@author: PC
"""

import numpy as np
from fractions import Fraction
from global_val import *
from excel import *
from matrix_revise import *

def cross_compare(file_name, mtr_name, units):
    n = len(units)
    a = np.zeros((n, n))
    a = load_excel(file_name, mtr_name,n)
    return a

def get_weight(a):
    n = a.shape[0]
    e_vals, e_vecs = np.linalg.eig(a)
    lamb = max(e_vals)
    w = e_vecs[:, e_vals.argmax()]
    w_tmp = w / np.sum(w)
    w = w_tmp.astype(float)
    ri = {1: 0, 2: 0, 3: 0.58, 4: 0.9, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49, 11: 1.51}
    cr = 0
    ci = 0
    if n > 2:
        ci = (lamb - n) / (n - 1)
        cr = ci / ri[n]

        if cr >= 0.1:
            w, cr = matrix_auto_adjust(a,w)
    return w, cr

def human_load_ahp():
    goal = config.get('Goal','goal')
    config.write(open(config.get('Path','path'), "w"))

    config.read(config.get('Path','path'), encoding="utf-8")
    criterions = config.options('Criterion')

    alternatives = config.options('Plan')
    n2 = len(criterions)
    n3 = len(alternatives)

    A = human_load_matrixs[goal]

    W2, cr2 = get_weight(A)

    alternatives_val = {}
    for index in range(n3):
        alternatives_val[alternatives[index]] = 0

    for i in range(n2):
        plans_str = config.get('Criterion', criterions[i])
        plans = plans_str.split('&')
        A_cri = human_load_matrixs[criterions[i]]
        w3, cr3 = get_weight(A_cri)
        for j in range(len(plans)):
            alternatives_val[plans[j]] = alternatives_val[plans[j]] + w3[j] * W2[i]
        plans.clear()

    for key in alternatives_val.keys():
        config.set('Plan', key, str(alternatives_val[key]))
    config.write(open(config.get('Path','path'), "w"))

def ahp(expert_name,expert_file_path):
    goal = config.get('Goal','goal')
    config.write(open(config.get('Path','path'), "w"))

    config.read(config.get('Path','path'), encoding="utf-8")
    criterions = config.options('Criterion')
    alternatives = config.options('Plan')

    n2 = len(criterions)
    n3 = len(alternatives)

    A = cross_compare(expert_file_path, goal, criterions)

    W2, cr2 = get_weight(A)

    alternatives_val = {}
    for index in range(n3):
        alternatives_val[alternatives[index]] = 0

    for i in range(n2):
        plans_str = config.get('Criterion', criterions[i])
        plans = plans_str.split('&')
        A_cri = cross_compare(expert_file_path, criterions[i], plans)
        w3, cr3 = get_weight(A_cri)
        for j in range(len(plans)):
            alternatives_val[plans[j]] = alternatives_val[plans[j]] + w3[j] * W2[i]
        plans.clear()

    for key in alternatives_val.keys():
        if not config.has_section(expert_name):
            config.add_section(expert_name)
        config[expert_name][key] = str(alternatives_val[key])
    config.write(open(config.get('Path','path'), "w"))

def group_decision():
    expert_num = len(experts)
    alternatives = config.options('Plan')
    weight_result = {}
    for index in range(len(alternatives)):
        weight_result[alternatives[index]] = 0

    sum_level = 0
    for expert in experts_name:
        sum_level += config.getint('Level',expert)
    for alt in alternatives:
        for expert in experts_name:
            if sum_level != 0:
                weight_result[alt] = weight_result[alt] + config.getfloat(expert, alt) * (config.getint('Level',expert)/sum_level)
            else:
                weight_result[alt] = weight_result[alt] + config.getfloat(expert, alt)
        if sum_level == 0:
            weight_result[alt] = weight_result[alt] / expert_num

        config.set('Plan',alt,str(weight_result[alt]))
    config.write(open(config.get('Path','path'), "w"))
