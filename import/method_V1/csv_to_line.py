import pandas as pd
#convert csv's to line protocol


# ====================================================
#convert sample data to line protocol (with nanosecond precision)
# df = pd.read_csv("data/BTC_sm_ns.csv")
# df["measurement"] = ['price' for t in range(len(df))]
# lines = [str(df["measurement"][d])
#          + ",type=BTC"
#          + " "
#          + "close=" + str(df["close"][d]) + ","
#          + "high=" + str(df["high"][d]) + ","
#          + "low=" + str(df["low"][d]) + ","
#          + "open=" + str(df["open"][d]) + ","
#          + "volume=" + str(df["volume"][d])
#          + " " + str(df["time"][d]) for d in range(len(df))]
# thefile = open('data/chronograf.txt', 'w')
# for item in lines:
#     thefile.write("%s\n" % item)

#covert full data to line protocol (with nanosecond precision)
# df_full = pd.read_csv("data/BTC_ns.csv")
# df_full["measurement"] = ['price' for t in range(len(df_full))]
# lines = [str(df_full["measurement"][d])
#          + ",type=BTC"
#          + " "
#          + "close=" + str(df_full["close"][d]) + ","
#          + "high=" + str(df_full["high"][d]) + ","
#          + "low=" + str(df_full["low"][d]) + ","
#          + "open=" + str(df_full["open"][d]) + ","
#          + "volume=" + str(df_full["volume"][d])
#          + " " + str(df_full["time"][d]) for d in range(len(df_full))]
# #append lines to a text file with DDL & DML:
# thefile = open('data/import.txt', 'a+')
# for item in lines:
#     thefile.write("%s\n" % item)


# ================================

import numpy as np
import pandas as pd
import time
import os
import string


'''
@brief:读取asc文件，将数据规整化，导出为CSV格式文件
@param:filePath - asc文件路径
@return: csvFile - 对于的csv文件
'''

# 计时开始
# start = time.clock()

# 使用生成器，而不是生成式
def get_line(df_full):
	line = []
	cols = df_full.columns.values.tolist()
	print(cols)		# ['Time', 'Point1', 'Point2', 'Point3', 'Point4', 'measurement']
	for row in range(len(df_full)):
		field = ""
		for col in range(1,len(cols)-1):
			field += (str(cols[col]) + "=" + str(df_full.iat[row, col])) + ","

		field = field.rstrip().strip(string.punctuation)
		line = [str(df_full["measurement"][row]) + ",type=test" 
				+ " " 
				+ field
				+ " " 
				+ str(df_full["Time"][row])]
		yield line


# --------------------------------------------------

asc_file = r'C:\Users\user\Desktop\ZYJ_InfluxDB\code\csv_test.csv'
# 导入文件
df_full = pd.DataFrame(pd.read_csv(asc_file,low_memory=False))
print("**********************")
print(df_full.loc[:3])

# 取列名，作为field字段名
# cols = df_full.columns.values.tolist()

# 表格名为input，(table/measurement)
df_full["measurement"] = ['input' for n in range(len(df_full))]
print("**********************")
print(df_full.loc[:3])
print("**********************")
print(df_full["Point3"][0:2])
lines = get_line(df_full)
print("----")
print(next(lines))
print("----")

#append lines to a text file with DDL & DML:
# thefile = open('import.txt', 'a+')
# for item in lines:
#     thefile.write("%s\n" % item)


# 计时结束
# end = time.clock()
# elapsed = end - start
# print("Time used:", elapsed)


