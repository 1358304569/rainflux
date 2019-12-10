#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'xiaozhou'
__mtime__ = '2019/1/4'
# xiaozhou conding for SRCC
# matplotlib画图测试
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ------------------------------先分箱----------------
# 得到最大值，分为16个区间，对每个区间中的值进行计数
def my_count(x):
    max_value = max(x)
    delta = float('{:.6f}'.format(max_value/16))
    bins = [delta*i for i in range(0,17)]
    cats = pd.cut(x,bins)
    counts = pd.value_counts(cats)
    return counts

# ------------------------------后画图----------------
# 得到的计数值（Series格式），
def my_plot(counts):
    # 纵轴: y: Mpa，即series.index
    # 横轴: x: count，即series.values
    x = list(counts.values)
    # bin的右顶点，
    y = [n.right for n in list(counts.index)]

    # 输出为文件
    out = [x,y]
    output = pd.DataFrame(out)
    output = output.T
    output.rename(columns={0:"count",1:"Mpa"},inplace=True)
    output.to_csv(r"D:\Project\Python\rainflow\data\cycle_count.csv",sep=',',index=None)

    # ----二维柱图
    # plt.bar(x,y)
    # 曲线图
    plt.plot(x,y)
    plt.savefig(r"D:\Project\Python\rainflow\data\xxx.png")
    # plt.show()


# -----------------------保存结果------------------

# def my_output(Fcounts):
#     out = pd.DataFrame(Fcounts)
#     out.to_csv(r"D:\Project\Python\rainflow\data\cycle_count.csv",sep=',')


F = 11.4245*np.random.rand(10000)
J = 4.5283*np.random.rand(10000)

# 得到最大值，
Fcounts = my_count(F)
Jcounts = my_count(J)
# 画图
my_plot(Fcounts)



# 测试Series的属性和方法
# print(type(Fcounts.index))          # <class 'pandas.core.indexes.category.CategoricalIndex'>
# print(list(Fcounts.index)[1])       # ((10.709, 11.423]
# n = list(Fcounts.index)[1]
# print(max(n))                       # Interval' object is not iterable
# print(n.right)                      # 11.423
