# /usr/bin/env python
# -*- coding:utf-8 -*-

"""
__title__ = ''
__author__ = 'xiaozhou'
__mtime__ = '2019/03/18'
# xiaozhou conding for SRCC
"""

# =========================Rainflow V1,GUI V1===========

import tkinter
from tkinter.constants import *
from tkinter import *
# from tkinter import ttk
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename
from tkinter.scrolledtext import ScrolledText
import tkinter.messagebox
from tkinter import END
import time
import MyRainflow


class my_gui():
    """docstring for my_gui
		@brief 使用GUI界面来输入原始数据文件和计算参数

  	"""

    # 构造函数
    def __init__(self, init_window_name):
        self.init_window_name = init_window_name

    def set_init_window(self):
        self.init_window_name.title("单通道雨流计算程序 - 小周 for SRCC")
        self.init_window_name.geometry('600x480+300+200')
        self.init_window_name.attributes('-alpha', 1)

        # 设置标签
        self.file_label = Label(self.init_window_name, text="请选择数据文件（asc格式）：", bg='lightblue')
        self.file_label.place(x=50, y=50, width=180, height=30)

        # 文件路径
        self.file_text = Label(self.init_window_name, text="", relief='groove', justify='left')

        self.file_text.place(x=50, y=90, width=400, height=30)
        self.file_button = Button(self.init_window_name, text="选择"
                                  , bg='lightblue', width=15, command=self.select_file_path)
        self.file_button.place(x=460, y=90, width=80, height=30)

        # point和bins参数
        self.point_label = Label(self.init_window_name, text="Point:", bg='lightblue')
        self.point_label.place(x=50, y=130, width=80, height=30)
        self.point_text = Entry(self.init_window_name)
        self.point_text.insert(END, "1")  # 默认从第一列开始
        self.point_text.place(x=140, y=130, width=80, height=30)

        self.bins_label = Label(self.init_window_name, text="Bins:", bg='lightblue')
        self.bins_label.place(x=250, y=130, width=80, height=30)
        self.bins_text = Entry(self.init_window_name)
        self.bins_text.insert(END, "16")  # 默认分箱为16
        self.bins_text.place(x=340, y=130, width=80, height=30)

        # PSD标签
        self.psd_title = Label(self.init_window_name, text="PSD参数", bg="lightblue", justify='left')
        self.psd_title.place(x=50, y=180, width=180, height=30)

        # fs参数
        self.fs1_label = Label(self.init_window_name, text="fs:", bg='lightblue')
        self.fs1_label.place(x=50, y=220, width=70, height=30)
        self.fs1_text = Entry(self.init_window_name)
        self.fs1_text.insert(END, "1024")  # 默认采样频率1024Hz
        self.fs1_text.place(x=130, y=220, width=70, height=30)

        # noverlap参数
        self.noverlap_label = Label(self.init_window_name, text="noverlap:", bg='lightblue')
        self.noverlap_label.place(x=220, y=220, width=70, height=30)
        self.noverlap_text = Entry(self.init_window_name)
        self.noverlap_text.insert(END, "50")  # 默认混叠率50%
        self.noverlap_text.place(x=300, y=220, width=70, height=30)

        # nfft参数
        self.nfft_label = Label(self.init_window_name, text="nfft:", bg='lightblue')
        self.nfft_label.place(x=390, y=220, width=70, height=30)
        self.nfft_text = Entry(self.init_window_name)
        self.nfft_text.insert(END, "8192")  # 默认
        self.nfft_text.place(x=470, y=220, width=70, height=30)

        # 滤波标签
        self.psd_title = Label(self.init_window_name, text="滤波器参数", bg="lightblue", justify='left')
        self.psd_title.place(x=50, y=270, width=180, height=30)

        # fs参数
        self.fs2_label = Label(self.init_window_name, text="fs:", bg='lightblue')
        self.fs2_label.place(x=50, y=310, width=70, height=30)
        self.fs2_text = Entry(self.init_window_name)
        self.fs2_text.insert(END, "1024")  # 默认采样频率1024Hz
        self.fs2_text.place(x=130, y=310, width=70, height=30)

        # cut_freq参数
        self.cut_freq_label = Label(self.init_window_name, text="cut_freq:", bg='lightblue')
        self.cut_freq_label.place(x=220, y=310, width=70, height=30)
        self.cut_freq_text = Entry(self.init_window_name)
        self.cut_freq_text.insert(END, "90")  # 默认截止频率90Hz
        self.cut_freq_text.place(x=300, y=310, width=70, height=30)

        # order参数
        self.order_label = Label(self.init_window_name, text="order:", bg='lightblue')
        self.order_label.place(x=390, y=310, width=70, height=30)
        self.order_text = Entry(self.init_window_name)
        self.order_text.insert(END, "8")  # 默认
        self.order_text.place(x=470, y=310, width=70, height=30)

        # 设置确定/取消按钮
        self.finish_button = Button(self.init_window_name, text="确定", bg='lightblue', width=15,
                                    command=self.start_rainflow_main)  # command=self.test
        self.finish_button.place(x=460, y=430, width=80, height=30)  #
        self.cancel_button = Button(self.init_window_name, text="取消", bg='lightblue', width=15,
                                    command=self.init_window_name.quit)
        self.cancel_button.place(x=370, y=430, width=80, height=30)  #


    # 选择数据文件
    def select_file_path(self):
        self.file_path = askopenfilename()
        self.file_text.config(text=self.file_path)


    def start_rainflow_main(self):

        # 测试
        # print(self.file_text['text'], int(self.point_text.get()), int(self.bins_text.get())
        #     , int(self.fs1_text.get()), int(self.noverlap_text.get()), int(self.nfft_text.get())
        #     , int(self.fs2_text.get()), int(self.cut_freq_text.get()), int(self.order_text.get()))

        MyRainflow.main(self.file_text['text'], int(self.point_text.get()), int(self.bins_text.get())
            , int(self.fs1_text.get()), int(self.noverlap_text.get()), int(self.nfft_text.get())
            , int(self.fs2_text.get()), int(self.cut_freq_text.get()), int(self.order_text.get()))





def gui_start():
    init_window = tkinter.Tk()
    main_gui = my_gui(init_window)
    main_gui.set_init_window()
    init_window.mainloop()


if __name__ == '__main__':
    gui_start()
