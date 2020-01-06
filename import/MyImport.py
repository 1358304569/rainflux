# coding -*- utf8 -*-

# ========================小周使用python操作influx的基础测试--2018-12-13-==============

import argparse
import time
import os
import random
import pandas as pd
import numpy as np
from influxdb import DataFrameClient
from influxdb import InfluxDBClient


def get_FileCreateTime(filePath):
    t = os.path.getctime(filePath)
    return t


def asc_to_df(asc_file, tags):
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

	# 增加 tag列

	cities = []
	for i in range(df_split.shape[0]):
		cities.append(random.choice(tags.get("cities")))
	df_split["cities"] = cities
	return df_split



# def add_tags(df, ):


def df_import(df, host, port):

	# 各个参数
	user = 'admin'
	password = 'admin'
	dbname = 'test'
	# protocol = 'json'


	# 连接
	client = DataFrameClient(host, port, user, password, dbname)

	# 截取demo测试
	df = df.iloc[:10000, :]
	# 写入数据
	client.write_points(df, 'conjunction_demo', tag_columns=["cities"], time_precision='ms', batch_size=5000)
	# client.write_points(json_body)

	# 查询数据
	# result_set = client.query("SELECT * FROM inputFromPython LIMIT 5")
	# return result_set


# df = pd.DataFrame(data=list(range(30)),index=pd.date_range(start='2014-11-16', periods=30, freq='H'))
# df_import()


def main(asc_file, host='localhost', port=8086):

	tags = {
		"carriages": [93101, 91386],
		"stations": ["莘庄", "上海南站", "汶水路"],
		"cities": ["上海", "重庆", "广州",  "九江",  "南昌",  "深圳", "曼哈顿"]
	}


	# convert local asc file to dataframe format
	df = asc_to_df(asc_file, tags)


	# test
	# print(df.iloc[-5:,:])
	# print(df.iloc[:5,:])

	# import dataframe into influxdb
	df_import(df, host, port)


# 2019-12-19 mac路径
asc_file = r'/Users/zhouyijian/Desktop/data/point_19-22_little.asc'



# cmd启动参数
def parse_args():
    """Parse the args from main."""
    parser = argparse.ArgumentParser(
        description='example code to play with InfluxDB')
    parser.add_argument('--host', type=str, required=False,
                        default='localhost',
                        help='hostname of InfluxDB http API')
    parser.add_argument('--port', type=int, required=False, default=8086,
                        help='port of InfluxDB http API')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(asc_file, host=args.host, port=args.port)


# DataFrameClient —— write_point 用法
# write_points(dataframe, measurement, tags=None, tag_columns=None, 
#field_columns=None, time_precision=None, database=None, retention_policy=None, 
#batch_size=None, protocol=u'line', numeric_precision=None)