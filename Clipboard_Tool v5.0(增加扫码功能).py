#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
该文件为主要文件，程序目前功能很少，
后期可能会增添功能并优化代码，现有如下功能：
1.Translate(自动读取剪贴板内容并翻译，翻译的语言可自行添加英文缩写到 self.cb.addItems(["zh","en","jp"]) )
2.ScanImage(自动读取剪贴板图片并扫码，返回QRcode)
"""

import sys
import cv2
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel,QTextBrowser, QVBoxLayout,QHBoxLayout,QLineEdit,QPushButton,QComboBox,QMainWindow)
from PyQt6.QtGui import QIcon,QPixmap,QAction
from zxing import BarCodeReader
from pyzbar import pyzbar
from xpinyin import Pinyin
import Baidu_Text_transAPI


# 逻辑
fanyi = Baidu_Text_transAPI.Fanyi_Api()
class logic:
    def requests_fanyi(self, text, to_text='auto'):
        return fanyi.run(text, to_text=to_text)

    def pinyin(self, text):
        text_pinyin = Pinyin().get_pinyin(u"{}".format(text), tone_marks='marks')
        if text_pinyin != text:
            return text_pinyin, text
        else:
            return None

    def language(self, text): # 暂无用
        if text.isdigit() is not True:
            for ch in text:
                if u'\u4e00' <= ch <= u'\u9fff':
                    print('True')
                    return True
            else:
                if 'http' not in text:
                    print('False')
                    return False

    def scan_image(self,path):
        qrcode = cv2.imread(path) # 读取图片
        data = pyzbar.decode(qrcode)# 解析数据
        # text = data[0].data.decode('utf-8') # 在数据中解析出二维码的data信息
        if len(data) == 1:
            return data[0].data.decode('utf-8')
        elif len(data) > 1:
            data_list = [i.data.decode('utf-8') for i in data]
            return data_list
        else:
            return '图片未包含二维码信息'


class MyWindow(logic,QMainWindow):
    def __init__(self):
        super().__init__()
        self.label1 = None
        self.button_label1 = None
        self.label2 = None
        self.cb = None
        self.to_text = 'auto'
        self.save_image_path = './QRcode.jpg'
        self.automatic = 0
        self.initUI()

    def on_clipboard_change(self):
        clipboard = QApplication.clipboard() # 获取剪贴板信息
        if clipboard.mimeData().hasImage():
            self.scan_image_ui()
            image = clipboard.image()
            image.save(self.save_image_path)
            return_code_data = self.scan_image(self.save_image_path)
            if type(return_code_data) == str:
                self.text_brower.setText(return_code_data)
            elif type(return_code_data) == list:
                for i in return_code_data:
                    self.text_brower.append(str(i))
        else:
            if 'http' not in clipboard.text():
                self.translate_ui()
                if self.automatic == 0:
                    o_text, e_text = self.requests_fanyi(clipboard.text(),to_text=self.to_text)
                    print(o_text, e_text)
                    self.label1.setText(o_text)
                    self.label2.setText(e_text)
                elif self.automatic == 1:
                    self.label1.setText(clipboard.text())

        self.activateWindow()# 窗口跳到最前面



    def initUI(self):
        self.setWindowTitle('欸嘿是什么意思嘛~')
        self.setGeometry(750, 600, 485, 199)

        # 检测剪贴板
        clipboard = QApplication.clipboard()
        clipboard.dataChanged.connect(self.on_clipboard_change)

        main_ui = self.menuBar()
        translate = main_ui.addMenu('Translate')
        scanimage = main_ui.addMenu('ScanImage')

        go_translate_ui = QAction('切换',self)
        translate.addAction(go_translate_ui)
        go_translate_ui.triggered.connect(self.translate_ui)

        go_scanimage_ui = QAction('切换',self)
        scanimage.addAction(go_scanimage_ui)
        go_scanimage_ui.triggered.connect(self.scan_image_ui)


    def translate_ui(self):
        self.widget_for_translate = QWidget()
        self.horizontal = QHBoxLayout() # 水平布局
        self.label1 = QLineEdit('Waiting for clipboard changes...',self.widget_for_translate) # 设置输入框
        self.horizontal.addWidget(self.label1)
        self.label2 = QLabel('Waiting for clipboard changes...',self.widget_for_translate)

        self.button_label1 = QPushButton("Translate", self.widget_for_translate)  # 设置按钮
        self.horizontal.addWidget(self.button_label1)
        self.button_label1.clicked.connect(self.show_lable1_text)

        self.cb = QComboBox(self.widget_for_translate)
        self.cb.addItem('auto')
        self.cb.addItems(["zh","en","jp"])
        self.cb.currentIndexChanged.connect(self.language_code)
        self.horizontal.addWidget(self.cb)

        self.autotranslate_arg = QComboBox(self.widget_for_translate)
        self.autotranslate_arg.addItem('自动翻译')
        self.autotranslate_arg.addItems(['ON','OFF'])
        self.autotranslate_arg.currentIndexChanged.connect(self.auto_translate_arg)
        self.horizontal.addWidget(self.autotranslate_arg)

        # 布局样式
        self.vbox = QVBoxLayout() # 垂直布局
        self.vbox = QVBoxLayout(self.widget_for_translate)
        self.vbox.addLayout(self.horizontal)
        self.vbox.addWidget(self.label2)

        # self.setLayout(self.vbox)

        self.setCentralWidget(self.widget_for_translate)

    def language_code(self):
        self.to_text = self.cb.currentText()

    def auto_translate_arg(self):
        if self.autotranslate_arg.currentText() == 'ON':
            self.automatic = 0
        elif self.autotranslate_arg.currentText() == 'OFF':
            self.automatic = 1


    def show_lable1_text(self):
        o_text, e_text = self.requests_fanyi(self.label1.text(),to_text=self.to_text)
        print(o_text, e_text)
        self.label1.setText(o_text)
        self.label2.setText(e_text)


    def scan_image_ui(self):
        widget_for_image = QWidget()
        horizontal = QHBoxLayout(widget_for_image)
        self.text_brower = QTextBrowser(widget_for_image)
        horizontal.addWidget(self.text_brower)

        self.setCentralWidget(widget_for_image)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.showNormal()
    sys.exit(app.exec()) # 重点！！！是exec()，不要再因为这个错误恶心自己一上午了
