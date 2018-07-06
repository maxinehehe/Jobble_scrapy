#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-7-1 下午5:49
# @Author  : maxinehehe
# @Site    : 
# @File    : main.py
# @Software: PyCharm

from scrapy.cmdline import execute
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# os.path.abspath(__file__)  获取当前文件的绝对路径
# os.path.dirname()  获取括号内 文件的上一级路径 即是所在目录
execute(["scrapy", "crawl", "jobbole"])  # 【命令终端】启动爬虫 scrapy crawl 爬虫名称