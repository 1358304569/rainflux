#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:zhouyijian
# datetime:2020-03-06 17:43
# software: IntelliJ IDEA


import argparse
import time
import os
import random
from functools import partial

import pandas as pd
import numpy as np
from influxdb import DataFrameClient
from influxdb import InfluxDBClient


def get_FileCreateTime(filePath):
    t = os.path.getctime(filePath)
    return t


def asc_to_df(asc_file):
    # 获取开始时间
    time_creative = get_FileCreateTime(asc_file)
    start_time = time.strftime("%Y--%m--%d %H:%M:%S", time.localtime(time_creative))

    # 倒入文件
    df = pd.DataFrame(pd.read_csv(asc_file, header=None, names=['Point']))

    # 预处理，删除表头，获取时间戳
    # 读取END所在行的行数
    line_end = df[df['Point'].isin(['END'])].index.values
    # 删除前面几行表头
    df_data = df.drop(np.arange(line_end+1), inplace=False)
    # 获取结束时间戳
    end_timestamp = time_creative + int(len(df_data)/1024)
    end_time = time.strftime("%Y--%m--%d %H:%M:%S", time.localtime(end_timestamp))

    # freq = str((int(end_timestamp) - int(time_creative))/len(df_data))+'s'

    # 设置可能的列粗
    columns_family = ['Point1', 'Point2', 'Point3', 'Point4', 'Point5', 'Point6', 'Point7', 'Point8', 'Point9', 'Point10',
                      'Point11', 'Point12', 'Point13', 'Point14', 'Point15', 'Point16', 'Point17', 'Point18', 'Point19', 'Point20',
                      'Point21', 'Point22', 'Point23', 'Point24', 'Point25', 'Point26', 'Point27', 'Point28', 'Point29', 'Point30',
                      'Point31', 'Point32', 'Point33', 'Point34', 'Point35', 'Point36', 'Point37', 'Point38', 'Point39', 'Point40',
                      'Point41', 'Point42', 'Point43', 'Point44', 'Point45', 'Point46', 'Point47', 'Point48', 'Point49', 'Point50',
                      'Point51', 'Point52', 'Point53', 'Point54', 'Point55', 'Point56', 'Point57', 'Point58', 'Point59', 'Point60',
                      'Point61', 'Point62', 'Point63', 'Point64', 'Point65', 'Point66', 'Point67', 'Point68', 'Point69', 'Point70',
                      'Point71', 'Point72', 'Point73', 'Point74', 'Point75', 'Point76', 'Point77', 'Point78', 'Point79', 'Point80',
                      'gps:Latitude', 'gps:Longitude', 'gps:Altitude', 'gps:EastVelocity', 'gps:NorthVelocity', 'gps:UpVelocity',
                      'gps:NumberOfSatellites', 'gps:Speed']

    # 分裂
    df_split = pd.DataFrame((x.split() for x in df_data['Point']),
                            index=pd.date_range(start=start_time, periods=len(df_data), end=end_time))

    # 修改列名
    df_split.columns = columns_family[:df_split.columns.size]

    return df_split



def format_data(row,k=1):
    data = row
    data = '{:.8f}'.format(float(data))   # 6位小数的精度不够，取8位
    data = round(float(data)*float(k), 8)
    return data



def main(asc_file):


    # convert local asc file to dataframe format
    df = asc_to_df(asc_file)

    # print("========切片========")
    # point = df.iloc[:5,:1]
    # print(type(point))
    # print(point)
    # point_lst = point.values.tolist()
    # print(point_lst)
    #
    # print("========选择=======")
    point_2 = df.iloc[:,1]
    point_lst_2 = point_2.values.tolist()
    #
    # print(type(point_2))
    # print(point_2)
    # print(point_lst_2)

    ylst = list(map(format_data, point_lst_2))

    # print(ylst)

    return ylst

# 2019-12-19 mac路径
asc_file = r'/Users/zhouyijian/Desktop/data/point_19-22_little.asc'


if __name__ == '__main__':
    main(asc_file)


# DataFrameClient —— write_point 用法
# write_points(dataframe, measurement, tags=None, tag_columns=None,
#field_columns=None, time_precision=None, database=None, retention_policy=None,
#batch_size=None, protocol=u'line', numeric_precision=None)