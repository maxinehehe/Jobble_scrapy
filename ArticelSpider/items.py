# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

"""
该文件定义了抓待取域的模型   类似javabean
"""
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join

import datetime
import re


def return_value(value):
    # 小技巧
    return value

class ArticelspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

def add_jobbole(self, value):
    return value + "-jobbole"


def date_convert(value):
    try:
        create_date = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_date = datetime.datetime.now()
    return create_date

def get_nums(value):
    # 可共用 提取数字
    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums

# 如果每一个都去第一个值 是否都要自己去写每个TakeFirst() 当然不用scrapy.ItemLoader提供了对其进行重载
class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()  # 默认取第一个

def remove_comment_tags(value):
    # 去掉tag中提取的评论
    if "评论" in value:
        return ""
    else:
        return value

# item用于组织
class JobboleArticleItem(scrapy.Item):
    # item只有一种类型 统一为Field 可以接受任何类型 类似字典形式

    title = scrapy.Field(
        # 自定义对title预处理 在末尾添加标示

        # MapCompose()可以从左到右调用函数 进行处理 title 注意：MapCompose可以调用多个函数
        # input_processor = MapCompose(add_jobbole)  # 一种方法
        input_processor = MapCompose(lambda x:x + "-jobbole")  # 一种方法

    )
    create_date = scrapy.Field(
        # 预处理时间 2017/2/23 成 2017-2-23
        input_processor = MapCompose(date_convert),  # 此处相当于参数
        # output_processor = TakeFirst()
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    # front_image_url必须是list 若用default_input_processor会导致下载出错
    # 覆盖掉之前的方法
    front_image_url = scrapy.Field(
        output_processor=MapCompose(return_value)  # 覆盖掉 default_input_processor
    )
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field(
        input_processor=MapCompose(get_nums),  # 此处相当于参数
    )
    comment_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)  # 此处相当于参数
    )
    fav_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)  # 此处相当于参数
    )
    tags = scrapy.Field(
        # tag_list 转变
        # 转变前：['职场 2 评论 程序员计算机专业']
        # 转变后：'职场 2 评论 程序员计算机专业'
        input_processor = MapCompose(remove_comment_tags),
        output_processor = Join(",")
    )
    content = scrapy.Field()

