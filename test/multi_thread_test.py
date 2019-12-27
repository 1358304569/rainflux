#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:zhouyijian
# datetime:2019-12-18 21:00
# software: IntelliJ IDEA

# python多线程测试



import threading



def thread_job():
    print("this is added thread, No. %s"%threading.current_thread())


def sys_info():
    '''
    @查看系统线程信息
    :return:
    '''
    added_thread = threading.Thread(target=thread_job(), name="T1 ")
    added_thread.start()
    print(threading.active_count())
    # print(threading.enumerate())
    # print(threading.current_thread())


if __name__ == '__main__':
    sys_info()
