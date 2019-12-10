import pandas as pd
import numpy as np




# 科学计数法==》浮点数
def format_data(row):
	data = row.strip()
	# print(data)
	data = '{:.8f}'.format(float(data))   # 6位小数的精度不够
	data = float(data)
	# print(data)
	return data



'''
四点循环计数法
2018-12-17
xiaozhou
'''



# 判断相邻三点是否为同一个趋势
def same_tendency(df, i):
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
    for j in range(begin, n - 3):
        s1 = abs(df.iloc[j+1, 0] - df.iloc[j+2, 0])
        s0 = abs(df.iloc[j+3, 0] - df.iloc[j, 0])
        # if s1 <= s0:
        if s1 < s0:
            flag = True
            break
        else:
            flag = False
            break

    return flag

# 剔除值
def drop_line(df, value):
    value_list = []
    value_list.append(value)
    value_line = dfB[dfB.isin(value_list)].index.values
    # 删除nan值
    df = df.drop(value_line)
    return  df

# 源文件
# 【2，4，1，3，4，6，8，5，6，2，1，4，7，2】
# csv_file = r'D:\Project\Python\rainflow\data\little_test.csv'
# 真实数据：5 千多行 x 5 列（time,point19-22）
csv_file = r'C:\Users\Administrator\Desktop\origin_data\point_19-22_very_little.csv'

# 读取为dataframe
# 原始数据：
ori_df = pd.DataFrame(pd.read_csv(csv_file, header=None))
# 取其中一列
ori_df = ori_df.iloc[1:,1]
ori_df = pd.DataFrame(list(map(format_data,ori_df)))


dfA = ori_df.copy(deep=True)
dfB = ori_df.copy(deep=True)
len_A = len(ori_df)


# 步骤一
# 对载荷时间历程进行处理，转换为峰谷值序列

m = len_A
for i in range(1,m-1):
    # 等值处理---暂时不用，因为数据中没有完全相等的值，只有忽略精度才相等
    # if ori_df.iat[i+1, 0] == ori_df.iat[i, 0]:
    #     dfB.ix[i, 0] = np.nan
    # 峰谷值处理
    if same_tendency(ori_df, i):
        dfB.iloc[i, 0] = np.nan

# 处理完后，B =【2，4，1，nan，nan，nan，8，5，6，nan，1，nan，7，2】
# 删除nan值所在行
# 不用调用函数，自带dropna方法
# dfB = drop_line(dfB, np.nan)

dfB = dfB.dropna()
# 处理完后，B =【2，4，1，8，5，6，1，7，2】
n = len(dfB)
dfB['index'] = range(dfB.shape[0])
dfB.set_index('index', inplace=True)

# 步骤二
# dfD = dfB.copy(deep=True)

# 幅值列表
F = []
# 均值列表
J = []
# 设置cycle-count 的起点，默认从第一个点开始
global begin
begin = 0
while(True):
    if isRangepair(dfB):
        for j in range(begin, n - 3):
            s1 = abs(dfB.iloc[j + 1, 0] - dfB.iloc[j + 2, 0])
            s0 = abs(dfB.iloc[j + 3, 0] - dfB.iloc[j, 0])
            e3 = float((dfB.iloc[j+1] + dfB.iloc[j+2])/2)
            if s1 <= s0:
                F.append(s1)
                J.append(e3)

                # dfB = drop_line(dfB, dfB.ix[j+1])
                # dfB = drop_line(dfB, dfB.ix[j+2])
                # 删除这两个数
                dfB = dfB.drop([j+1,j+2])
                n = len(dfB)
                dfB['index'] = range(dfB.shape[0])
                dfB.set_index('index', inplace=True)

                # 剔除一对range-pair后，再应该从哪开始？
                # 试试从0
                begin = 0
                break
            else:
                continue
    # else:
    #     break
    # continue
    # 实际数据结果为空，就是因为第一次计数时，前4个点中，不成立range-pair，导致break直接结束了while循环
    # 这个continue是为了循环中 drop后，继续
    # 改进一下，判断一下是否到最后4个点，未到的话，则继续
    elif len(dfB) >= 4:
        # 到这里说明不成立range-pair，那就从下一个点 begin，
        begin += 1
        pass
    else:
        break
    if len(dfB) < 4:
        break
    continue


# 步骤三，显示结果
print(F)
print(J)



