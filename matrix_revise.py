# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 12:56:10 2021

@author: PC
"""

import numpy as np
import math

ri = {3: 0.58, 4: 0.9, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49, 11: 1.51}
def matrix_hadamard(a,A,ratio):
    n = a.shape[0]
    b = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            b[i,j] = math.pow(a[i, j], (1 - ratio)) * math.pow(A[i, j], ratio)
    e_vals, e_vecs = np.linalg.eig(b)
    lamb = max(e_vals)
    w = e_vecs[:, e_vals.argmax()]
    w = w / np.sum(w)
    w_result = w.astype(float)
    ci = (lamb - n) / (n - 1)
    cr = ci / ri[n]
    if isinstance(cr,np.complex):
        cr = cr.real
    if cr >= 0.1:
        return False, w_result, cr
    else:
        return True, w_result, cr

def matrix_auto_adjust(a,w):
    n = a.shape[0]
    a_tmp = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            a_tmp[i,j] = w[i]/w[j]

    reversion_ratio = 1
    low_ratio = 0
    high_ratio = 1
    previous_low = 0
    previous_high = 0
    best_w = None
    best_cr = 0

    while low_ratio < high_ratio and (low_ratio != previous_low or high_ratio != previous_high):
        mid = (low_ratio + high_ratio) / 2
        mid_ratio = round(mid,1)
        is_pass,w,cr = matrix_hadamard(a,a_tmp,reversion_ratio)
        previous_low = low_ratio
        previous_high = high_ratio
        if is_pass == False:
            low_ratio = mid_ratio
        if is_pass == True:
            high_ratio = mid_ratio
            best_w = w
            best_cr = cr
        reversion_ratio = mid_ratio

    return best_w, best_cr
