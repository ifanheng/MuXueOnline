#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: 范恒
# 日期与时间：2020/3/18 16:56
# 什么程序创建：PyCharm
# 作用：

import json

import requests


def send_single_sms(apikey, code, mobile):
    # 发送单条短信
    url = "https://sms.yunpian.com/v2/sms/single_send.json"
    text = "【go语言站点】您的验证码是%s。如非本人操作，请忽略本短信" % code

    # res = requests.post(url, data={
    #     "apikey": apikey,
    #     "mobile": mobile,
    #     "text": text
    # })

    tmp_dict = {"code": 0, "msg": "发送成功", "count": 1, "fee": 0.05, "unit": "RMB", "mobile": "17867918086", "sid": 52201691436}
    # re_json = json.loads(res.text)
    return tmp_dict
