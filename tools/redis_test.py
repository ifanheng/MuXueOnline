#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: 范恒
# 日期与时间：2020/3/19 1:41
# 什么程序创建：PyCharm
# 作用：

import redis
import time

r = redis.Redis(host='localhost', port=6379, db=0, charset="utf8", decode_responses=True)
r.set("mobile", "123")

# 配置1秒之后过期
r.expire("mobile", 1)
print(r.get("mobile"))
print(r.get("mobile"))
print(r.get("mobile"))
time.sleep(1)
print(r.get("mobile"))

