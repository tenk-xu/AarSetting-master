#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Python3.x 导入方法
from tkinter import *
from tenk.overseaTest import transPackage


def trans():
    srcPath = init_data_Text.get(1.0, END).strip().replace("\n", "")
    print(srcPath)
    config = config_data_Text.get(1.0, END).strip().replace("\n", "")
    print(config)
    transPackage.main(srcPath, config)

def deletes():
    srcPath = init_data_Text.get(1.0, END).strip().replace("\n", "")
    print(srcPath)
    config = config_data_Text.get(1.0, END).strip().replace("\n", "")
    print(config)
    transPackage.deletes(srcPath, config)

root = Tk()  # 创建窗口对象的背景色
#窗口名
root.title("oversea-tool-v1.0")
# 定义窗口弹出时的默认展示位置
root.geometry('1068x681+300+100')

# 标签
init_data_label = Label(root, text="待处理文件路径")
init_data_label.grid(row=0, column=0)
config_data_label = Label(root, text="替换配置数据")
config_data_label.grid(row=3, column=0)

# 文本框
init_data_Text = Text(root, width=60, height=10)  # 原始aar文件路径录入框
init_data_Text.grid(row=1, column=0, rowspan=2)
config_data_Text = Text(root, width=60)  # 替换文本录入框
config_data_Text.grid(row=4, column=0, rowspan=6)

# 按钮
trans_settings_button = Button(root, text="替换", bg="lightyellow", width=10, command=trans)  # 调用内部方法  加()为直接调用
trans_settings_button.grid(row=10, column=0)

# 删除按钮
delete_settings_button = Button(root, text="删除配置", bg="lightyellow", width=10, command=deletes)  # 调用内部方法  加()为直接调用
delete_settings_button.grid(row=11, column=0)

root.mainloop()  # 进入消息循环

class MY_GUI():
    def __init__(self,init_window_name):
        self.init_window_name = init_window_name