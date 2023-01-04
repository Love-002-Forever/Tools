#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
该文件为百度翻译api接口的代码文件，可正常使用，
"""

import random
import requests
from hashlib import md5


class Fanyi_Api:
    def __init__(self):
        self.appid = '' # 你自己的appid
        self.appkey = '' # 你自己的appkey
        self.salt = random.randint(32768, 65536)
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        self.url = 'https://api.fanyi.baidu.com/api/trans/vip/translate'

    def __make_md5(self, s, encoding='utf-8'):
        return md5(s.encode(encoding)).hexdigest()

    def __sign(self, query):  # 要翻译的内容
        return self.__make_md5(self.appid + query + str(self.salt) + self.appkey)

    def run(self, text, from_text='auto', to_text='auto'):
        sign = self.__sign(text)
        payload = {'appid': self.appid, 'q': text, 'from': from_text, 'to': to_text, 'salt': self.salt, 'sign': sign}

        resp = requests.post(self.url, params=payload, headers=self.headers).json()
        src = resp["trans_result"][0]["src"]
        dst = resp["trans_result"][0]["dst"]

        return src, dst


# fanyi = Fanyi_Api()
# print(fanyi.run('你好，世界'))
