#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:zhouyijian
# datetime:2019-12-13 11:21
# software: IntelliJ IDEA



# python enviorment test

import sys


# print(sys.version)
# print("hello world")


import random
a = [1, 2, 3, 4, 5, 6, 7, 8, 9]
b = random.sample(a, 1)



tags = {
		"carriages": [93101, 91386],
		"stations": ["莘庄", "上海南站", "汶水路"],
		"cities": ["上海", "重庆", "广州"]
	}

b = tags.keys()


print(b)


