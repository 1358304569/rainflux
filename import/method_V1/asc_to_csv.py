# -*- coding:utf-8 -*-
# Tools: PyCharm 2018.2
# Author: DING YI
___date__ = '2018/12/4 2:57'



import numpy as np
import pandas as pd
import time
import os

# 获取文件的创建时间
def get_FileCreateTime(filePath):
    t = os.path.getctime(filePath)
    return t

# 计时开始
# start = time.clock()

# 获取文件创建时间的时间戳
file_path = r'C:\Users\user\Desktop\ZYJ_InfluxDB\data\origin_data\point_19--22_part.asc'
time_creative = get_FileCreateTime(file_path)

# 导入文件
df = pd.DataFrame(pd.read_csv(file_path, header=None, names = ['Point']))

# 读取END所在行的行数
line_end = df[df['Point'].isin(['END'])].index.values
# print(line_end)

# 删除前面几行
df_data = df.drop(np.arange(line_end+1), inplace=False)

columns_family = ['Point1','Point2','Point3','Point4','Point5','Point6','Point7','Point8','Point9','Point10',
				'Point11','Point12','Point13','Point14','Point15','Point16','Point17','Point18','Point19','Point20',
				'Point21','Point22','Point23','Point24','Point25','Point26','Point27','Point28','Point29','Point30',
				'Point31','Point32','Point33','Point34','Point35','Point36','Point37','Point38','Point39','Point40',
				'Point41','Point42','Point43','Point44','Point45','Point46','Point47','Point48','Point49','Point50',
				'Point51','Point52','Point53','Point54','Point55','Point56','Point57','Point58','Point59','Point60',
				'Point61','Point62','Point63','Point64','Point65','Point66','Point67','Point68','Point69','Point70',
				'Point71','Point72','Point73','Point74','Point75','Point76','Point77','Point78','Point79','Point80',
				'gps:Latitude','gps:Longitude','gps:Altitude','gps:EastVelocity','gps:NorthVelocity','gps:UpVelocity','gps:NumberOfSatellites','gps:Speed']

# 分列，索引作为时间戳
# df_split = pd.DataFrame((x.split("   ") for x in df_data['Point']), index=((df_data.index-76)/1024+time_creative), columns=['Point1','Point2','Point3','Point4','Point5','Point6','Point7','Point8','Point9','Point10','Point11','Point12','Point13','Point14','Point15','Point16','Point17','Point18','Point19','Point20','Point21','Point22','Point23','Point24','Point25','Point26','Point27','Point28','Point29','Point30','Point31','Point32','Point33','Point34','Point35','Point36','Point37','Point38','Point39','Point40','Point41','Point42','Point43','Point44','Point45','Point46','Point47','Point48','Point49','Point50','Point51','Point52','Point53','Point54','Point55','Point56','Point57','Point58','Point59','Point60','Point61','Point62','Point63','Point64','Point65','Point66','Point67','Point68','Point69','Point70','Point71','Point72','Point73','Point74','Point75','Point76','Point77','Point78','Point79','Point80','gps:Latitude','gps:Longitude','gps:Altitude','gps:EastVelocity','gps:NorthVelocity','gps:UpVelocity','gps:NumberOfSatellites','gps:Speed'])
df_split = pd.DataFrame((x.split(" +") for x in df_data['Point']), index=((df_data.index-int(line_end)+1)/1024+time_creative))
# 结果仍有空格/制表符，使用\\s匹配任意空白。不行，结果后面无法分列，整个为一列了。
# df_split = pd.DataFrame((x.split("\\s+") for x in df_data['Point']), index=((df_data.index-int(line_end)+1)/1024+time_creative))


# 修改列名
df_split.columns = columns_family[:df_split.columns.size]
df_split.index.name = "Time"

# 导出csv
df_split.to_csv("./csv_test.csv", index=True, sep=',')

# 计时
# end = time.clock()
# elapsed = end - start
# print("Time used:", elapsed)