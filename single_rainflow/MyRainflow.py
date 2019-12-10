#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'xiaozhou'
__mtime__ = '2018/12/26'
# xiaozhou conding for SRCC
"""

import pandas as pd
import numpy as np
import time
import os
from scipy import signal
from matplotlib import pyplot as plt
from functools import partial
import msvcrt
import sys

# -----------------------------小工具-----------------------


# 科学计数法==》浮点数——带K 的
def format_data(row,k):
	data = row
	data = '{:.8f}'.format(float(data))   # 6位小数的精度不够，取8位
	data = round(float(data)*float(k), 8)
	return data


# 科学计数法==》浮点数——不带K 的
# def format_data(row):
# 	data = row
# 	data = '{:.8f}'.format(float(data))   # 6位小数的精度不够，取8位
# 	data = round(float(data)*0.071, 8)
# 	return data

# 获取文件绝对时间（创建/修改时间）
def get_FileCreateTime(filePath):
	t = os.path.getctime(filePath)
	return t


# 迭代器产生波形横坐标----------------测试
def my_range(m):
	yield range(1,m-1)


# -----------------------------------------读文件------------------
# 去表头
# 将asc文件读取为dataframe
def asc_to_df(asc_file):
	'''
	:param asc_file: 原始文件，多通道，带表头
	:return: 原始文件，去表头，多通道的dataframe格式
	'''
	# 获取开始时间
	time_creative = get_FileCreateTime(asc_file)
	start_time = time.strftime("%Y--%m--%d %H:%M:%S", time.localtime(time_creative))

	# 倒入文件
	df = pd.DataFrame(pd.read_csv(asc_file, header=None, names=['Point']))

	# 读取END所在行的行数
	line_end = df[df['Point'].isin(['END'])].index.values

	# 删除前面几行表头
	df_data = df.drop(np.arange(line_end+1), inplace=False)

	# 获取结束时间戳
	end_timestamp = time_creative + int(len(df_data)/1024)
	# end_time = time.strftime("%Y--%m--%d %H:%M:%S", time.localtime(end_timestamp))

	# freq = str((int(end_timestamp) - int(time_creative))/len(df_data))+'s'

	# 设置可能的列簇
	columns_family = \
		['Point1', 'Point2', 'Point3', 'Point4', 'Point5', 'Point6', 'Point7', 'Point8', 'Point9', 'Point10',
		'Point11', 'Point12', 'Point13', 'Point14', 'Point15', 'Point16', 'Point17', 'Point18', 'Point19', 'Point20',
		'Point21', 'Point22', 'Point23', 'Point24', 'Point25', 'Point26', 'Point27', 'Point28', 'Point29', 'Point30',
		'Point31', 'Point32', 'Point33', 'Point34', 'Point35', 'Point36', 'Point37', 'Point38', 'Point39', 'Point40',
		'Point41', 'Point42', 'Point43', 'Point44', 'Point45', 'Point46', 'Point47', 'Point48', 'Point49', 'Point50',
		'Point51', 'Point52', 'Point53', 'Point54', 'Point55', 'Point56', 'Point57', 'Point58', 'Point59', 'Point60',
		'Point61', 'Point62', 'Point63', 'Point64', 'Point65', 'Point66', 'Point67', 'Point68', 'Point69', 'Point70',
		'Point71', 'Point72', 'Point73', 'Point74', 'Point75', 'Point76', 'Point77', 'Point78', 'Point79', 'Point80',
		'gps:Latitude', 'gps:Longitude', 'gps:Altitude', 'gps:EastVelocity', 'gps:NorthVelocity', 'gps:UpVelocity',
		'gps:NumberOfSatellites', 'gps:Speed']


	# 分列，
	df_split = pd.DataFrame((x.split() for x in df_data['Point']),
							index=((df_data.index - int(line_end) + 1) / 1024 + time_creative))

	# 修改列名
	df_split.columns = columns_family[:df_split.columns.size]
	return df_split


# ------------------------------PSD计算---------------------------

def My_PSD(ylst, fs1, noverlap, nfft):
	'''
	:brief: 对单通道数据进行PSD计算
	:param ylst:单通道 y 轴数据
	:return Pxx:PSD结果的y 轴数据（功率）
			freqs:PSD结果的x 轴数据（频率）
			line: 暂无
	'''

	# fs = 1024  # 采样频率
	# noverlap = 50  # 50%的重叠
	# nfft = 8192  # delta_f = 1/T = fs/nfft = 0.125Hz
	window = np.hanning(nfft)  # 加窗
	# PSD计算
	[Pxx, freqs, line] = plt.psd(ylst, Fs=fs1, window=window, noverlap=noverlap, NFFT=nfft, return_line=True)
	return  [Pxx,freqs]

# ------------------------滤波-------------------------

def My_filter(ylst, fs2, cut_freq, filter_order):
    '''
    :param ylst:
    :return:
    '''
    # 原始采用频率为1024Hz，截止频率取90Hz，则wn = 2*90/1024约为0.088，滤波器阶词设置为8
    # filter_order = 8
    # cut_freq = 90
    # fs2 = 1024
    wn = float('{:.4f}'.format(2 * cut_freq / fs2))

    b, a = signal.butter(filter_order, wn, 'lowpass')		# 低通，
    filted_data = list(signal.filtfilt(b, a, ylst))
    return filted_data

'''
# ----------------四点循环计数法-------------------------
'''

# 判断相邻三点是否为同一个趋势
def same_tendency(ori_df, i):
	if (ori_df.iat[i-1, 0] < ori_df.iat[i, 0]) and (ori_df.iat[i, 0] < ori_df.iat[i+1, 0]):
		return True
	elif (ori_df.iat[i-1, 0] > ori_df.iat[i, 0]) and (ori_df.iat[i, 0] > ori_df.iat[i+1, 0]):
		return True

	else:
		return False


# 判断range-pair
def isRangepair(df):
	n = len(df)
	flag = False
	for j in range(begin,n-3):
		s1 = abs(df.iloc[j+1, 0] - df.iloc[j+2, 0])
		s0 = abs(df.iloc[j+3, 0] - df.iloc[j, 0])
		if s1 <= s0:
			flag = True
			break
		else:
			flag = False
			break

	return flag


# 剔除range-pair 值
def drop_line(df, value):
	value_list = []
	value_list.append(value)
	value_line = dfB[dfB.isin(value_list)].index.values
	# 删除nan值
	df = df.drop(value_line)
	return  df


# ----------------------雨流计数，四点法------------------
# 步骤一：对载荷时间历程进行处理，转换为峰谷值序列
def covert2_PV_Series(ori_df):
	'''
	:param ori_df:
	:return:
	'''
	# dfA = ori_df.copy(deep=True)
	dfB = ori_df.copy(deep=True)

	m = len(ori_df)
	# # for循环太慢，5万行要11s，一个源文件就要一个小时（预估）
	for i in range(1, m - 1):
		# 等值处理---暂时不用，因为数据中没有完全相等的值，只有忽略精度才相等
		# if ori_df.iat[i+1, 0] == ori_df.iat[i, 0]:
		#     dfB.ix[i, 0] = np.nan

		# 峰谷值处理
		if same_tendency(ori_df, i):
			dfB.iloc[i, 0] = np.nan
	dfB = dfB.dropna()
	return dfB


# 步骤二：判断并剔除range-pairs
def judge_del_rangePairs(dfB):
	# 幅值列表
	F = []
	# 均值列表
	J = []
	n = len(dfB)
	global begin
	begin = 0
	while (True):
		if isRangepair(dfB):
			for j in range(begin, n - 3):
				s1 = abs(dfB.iloc[j + 1, 0] - dfB.iloc[j + 2, 0])
				s0 = abs(dfB.iloc[j + 3, 0] - dfB.iloc[j, 0])
				e3 = float((dfB.iloc[j + 1] + dfB.iloc[j + 2]) / 2)
				if s1 <= s0:
					F.append(s1)
					J.append(e3)
					# # 删除这两个数
					dfB = dfB.drop([j+1, j+2])
					n = len(dfB)
					dfB['index'] = range(dfB.shape[0])
					dfB.set_index('index', inplace=True)
					begin = 0
					break
				else:
					continue

		# 改进一下，判断一下是否到最后4个点，未到的话，则继续
		elif len(dfB) > 4:
			# 到这里说明不成立range-pair，那就从下一个点 begin，
			begin += 1

			pass
		else:
			break
		if len(dfB) <= 4:
			break
		continue
	return [F, J]

'''
# ===============幅值和均值统计：分箱，计数================
'''
# ------------------------------先分箱----------------
# 得到最大值，分为16个区间，对每个区间中的值进行计数
def my_count(x, bins):
    max_value = max(x)
    delta = float('{:.6f}'.format(max_value/bins))
    bins = [delta*i for i in range(0,bins + 1)]
    cats = pd.cut(x,bins)
    counts = pd.value_counts(cats)
    return counts

# ------------------------------后画图----------------
# 得到的计数值（Series格式）
def my_plot(counts):
	# 纵轴: y: Mpa，即series.index
	# 横轴: x: count，即series.values
	x = list(counts.values)
	# bin的右顶点，
	y = [n.right for n in list(counts.index)]

	# 输出为文件
	out = [x, y]
	output = pd.DataFrame(out)
	output = output.T
	output.rename(columns={0: "count", 1: "Mpa"}, inplace=True)
	output.to_csv(r".\cycle_count.csv", sep=',', index=None)

	# ----二维柱图
	# plt.bar(x,y)
	# 曲线图
	plt.plot(x, y)
	plt.savefig(r".\Fcycle_count.png")

	# 显示图片
	# plt.show()


#
#--------------------------主程序---------------------
# 带K 的
def main(asc_file, point, k, bins, fs1, noverlap, nfft, fs2, cut_freq, filter_order):
# 不带K 的
# def main(asc_file, point, bins, fs1, noverlap, nfft, fs2, cut_freq, filter_order):

	# 读取为dataframe

	print("开始读取文件.....")
	df_file = asc_to_df(asc_file)

	# 取单通道，暂时测试数据只有一列，待使用多线程实现------------问题1
	print("取单通道.....")
	# single_point = df_file.iloc[:, 1]
	single_point = df_file.iloc[:, point]

	# 数据格式规整，科学计数法--> 浮点数
	print("数制转换.....")
	# 带K 的
	temp = partial(format_data, k)
	ylst = list(map(temp, single_point))

	# 不带K 的
	# ylst = list(map(format_data, single_point))

	# PSD计算
	print("开始PSD计算.....")
	[Pxx,freqs] = My_PSD(ylst, fs1, noverlap, nfft)

	# 得到波形开始平滑的点，作为低通截止频率，待实现------------问题2
	# cut_freq = get_fc(Pxx, freqs)
	# cut_freq = 20					# 此处将截止频率暂定为 20Hz,1号线大概我16Hz

	# 滤波
	print("开始滤波.....")
	ylst = My_filter(ylst, fs2, cut_freq, filter_order)

	# 雨流开始
	# 先读取为dataframe格式
	ori_df = pd.DataFrame(ylst)

	# 步骤一：转换为峰谷值序列
	print("开始峰谷值转换.....")
	dfB = covert2_PV_Series(ori_df)
	dfB['index'] = range(dfB.shape[0])
	dfB.set_index('index', inplace=True)

	# 步骤二：判断并剔除range-pairs
	print("开始判断并剔除range-pairs.....")
	[F, J] = judge_del_rangePairs(dfB)

	# ----------------
	# 得到计数结果
	Fcounts = my_count(F, bins)

	# 导出计数结果
	# Jcounts = my_count(J)
	# 画图
	my_plot(Fcounts)		# 暂时显示的是PSD图，而非rainflow图，

	# 退出
	print("请按任意键退出程序：")
	anykey = ord(msvcrt.getch())  # 此刻捕捉键盘，任意键退出
	if anykey in range(0, 256):
		print("Have a nice day =。=")
		time.sleep(1)
		sys.exit()


# ----------------------------入口--------------


