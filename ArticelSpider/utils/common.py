#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-7-4 下午4:25
# @Author  : maxinehehe
# @Site    : 
# @File    : common.py
# @Software: PyCharm

import hashlib

def get_md5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest() # 返回摘要

if __name__ == "__main__":
    print(get_md5("http://jobbole.com".encode("utf-8")))

# python3都是unicode