# coding -*- utf8 -*-

# ========================小周使用python操作influx的基础测试--2018-12-13-==============


import time
import os
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

	# 修改列明
	df_split.columns = columns_family[:df_split.columns.size]
	return df_split



def df_import(df):

	# 各个参数
	host = 'localhost'
	port = 8086
	user = 'test'
	password = 'test'
	dbname = 'test1'
	# protocol = 'json'
	# measurement = 'inputFromPython'

	# df = pd.DataFrame(data=list(range(14401)),
	# 	index=pd.date_range(start='2018-11-16 16:00:00', freq='s', end='2018-11-16 20:00:00'))
	

	# 连接
	# client = InfluxDBClient(host, port, user, password, dbname)	
	client = DataFrameClient(host, port, user, password, dbname)
	# 创建数据库
	# client.create_database(dbname)
	# 写入数据
	client.write_points(df, 'little', time_precision='ms', batch_size=65536)
	# client.write_points(json_body)
	# 查询数据
	# result_set = client.query("SELECT * FROM inputFromPython LIMIT 5")
	# return result_set


# df = pd.DataFrame(data=list(range(30)),index=pd.date_range(start='2014-11-16', periods=30, freq='H'))
# df_import()


def main(asc_file):
	df = asc_to_df(asc_file)
	print(df.iloc[-5:,:])
	print(df.iloc[:5,:])
	# print(df.index.values.tolist()[200])
	# df_import(df)
	# result_set = df_import(df)
	# print(type(result_set)



# asc_file = r'D:\Project\influx_test\point_19--22_part.asc'

# 2019-12-19 mac路径
asc_file = r'/Users/zhouyijian/Desktop/data/point_19-22_little.asc'



if __name__ == '__main__':
	main(asc_file)





# write_points(dataframe, measurement, tags=None, tag_columns=None, 
#field_columns=None, time_precision=None, database=None, retention_policy=None, 
#batch_size=None, protocol=u'line', numeric_precision=None)