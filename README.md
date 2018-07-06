基于scrapy进行爬取伯乐在线的最新文章 将每篇文章的缩略图保存至本地 异步处理爬取的数据保存至MySQL数据库。

一 。首先创建个人虚拟环境：
1.安装虚拟环境 virtualenvwrapper 【使用豆瓣源】

maxinehehe@maxinehehe-PC:~$  pip install -i https://pypi.douban.com.simple/ virtualenvwrapper

2.【windows忽略】修改bashrc文件

maxinehehe@maxinehehe-PC:~$  gedit ~/.bashrc

添加：
export WORKON_HOME=$HOME/.virtualenvs  # .virtualenvs是虚拟环境文件夹 可自己创建
source /media/maxinehehe/5C584003583FDB0A/python35/Scripts/virtualenvwrapper.sh     # 可通过 find / -name virtualenvwrapper.sh
maxinehehe@maxinehehe-PC:~$  source ~/.bashrc
使配置立即生效

3.创建虚拟环境【python3】
maxinehehe@maxinehehe-PC:~$  mkvirtualenv --python3=/usr/bin/python3 article_spider

4.查看或进入虚拟环境
maxinehehe@maxinehehe-PC:~$ workon
ArticelSpider
article_spider
py2scrapy
py3scrapy
maxinehehe@maxinehehe-PC:~$ workon article_spider
(article_spider) maxinehehe@maxinehehe-PC:~$ 

4.创建爬虫工程项目【pip install -i 豆瓣源 scrapy】

maxinehehe@maxinehehe-PC:~$ scrapy startproject ArticleSpider

5.创建新的爬虫 
maxinehehe@maxinehehe-PC:~$ scrapy genspider jobbole http://blog.jobbole.com/all-posts/
根据模板生成一个新的爬虫


当前文件目录如下：



5.目录结构理解
spiders 
jobbole.py
文件夹下放的是实际的爬虫代码，处理爬虫的逻辑，比如使用正则表达式或xpath,css等选择器爬取内容。
class JobboleSpider(scrapy.Spider):    # 模板
    name = 'jobbole'
    # 允许域名
    allowed_domains = ['blog.jobbole.com']
    # 起始URL
    start_urls = ['http://blog.jobbole.com/all-posts/']
    # 解析函数 解析网址
    def parse(self, response):
    	    # 解析列表页中的所有文章URL 拿到当前页文章的网址列表数组
post_nodes = response.css("#archive .floated-thumb .post-thumb a")  # 获取节点
# 该节点包含 图片地址 和 文件详情地址
# '<a target="_blank" href="http://blog.jobbole.com/114194/" title="深入学习 Redis（3）：主从复制"><img #src="http://jbcdn2.b0.upaiyun.com/2016/04/49961db8952e63d98b519b76a2daa5e2.png" alt="" width="120" height="120"></a>'
for post_node in post_nodes:
    image_url = post_node.css("img::attr(src)").extract_first("")  # extract()[0]  # 提取图片地址 
    post_url = post_node.css("::attr(href)").extract_first("")  # 提取文章详情地址
    yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url":image_url}, callback=self.parse_detail)
    #  parse.urljoin(a,b)   比如 a = http://blog.jobbole.com b=11203 4 即是将二者连接成 http://blog.jobbole.com/112034
    # 若 a=http://blog.jobbole.com b=http://blog.jobbole.com/112034 则结果为http://blog.jobbole.com/112034
    # 所以用parse.urljoin()可以解决很多当前路径或者非当前路径问题
    # meta 信息则会传递到request中 以便其它函数调用其中信息
    # callback则是表示 回调函数 即调取哪一个函数来处理当前的url 
# 下面是xpath和css两种选择器的取法
# next_url = response.xpath('//*[@id="archive"]/div[@class="navigation margin-20"]/a[@class="next page-numbers"]/@href').extract()[0]
next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
print("下一页："+next_url+"\n")
if next_url:
    # http://blog.jobbole.com/all-posts/page/2/
    # 拿到下一页 交给scrapy下载器
    # yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse) # 传函数名即可 由底层twisted调用
    # 错误原因 由于传递的是post_url始终转回爬取这一页 而next_url并未传递过去
    # 如果继续传入 post_url【已爬取】scrapy会自动判断 为已经爬去 则终止爬虫运行
    yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)  # 传函数名即可 由底层twisted调用
    # 此处调取parse函数因为 这里需要回调处理文章列表页的函数 

为什么使用yield?
上面可以看出算是递归的形式的，如果网站待爬取条目趋近于无穷，那么这样的递归是无法想象的，还没等爬取，内存就已经溢出了。使用yield生成器则可以 使用的时候调取一次 不使用就不进行储存生成，极大地节省了空间，同时提高了程序运行效率。
def parse_detail(self, response):
    """
    提取文章的具体字段
    :param response:
    :return:
    """
    # 编写数据的解析和爬取
    article_item = JobboleArticleItem() # 实例化
    front_image_url = response.meta.get("front_image_url", "")  # 第二个“”是默认值   文章封面图
    # 通过item_loader加载item
    # 传递 实例化对象
    # ArticleItemLoader
    item_loader = ArticleItemLoader(item=JobboleArticleItem(), response=response)

    # 统一使用css
    item_loader.add_css("title", ".entry-header h1::text")
    item_loader.add_value("url", response.url)
    item_loader.add_value("url_object_id", get_md5(response.url))
    item_loader.add_css("create_date", "p.entry-meta-hide-on-mobile::text")
    item_loader.add_value("front_image_url", [front_image_url])
    item_loader.add_css("praise_nums", ".vote-post-up h10::text")
    item_loader.add_css("comment_nums", "a[href='#article-comment'] span::text")
    item_loader.add_css("fav_nums", ".bookmark-btn::text")
    item_loader.add_css("tags", "p.entry-meta-hide-on-mobile a::text")
    item_loader.add_css("content", "div.entry")
    # 进行解析
    article_item = item_loader.load_item()
    # 只有调用load_item()方法才会对item进行解析
    yield article_item   # 会传送到pipelines
# 此处需要说明的是为什么要使用ItemLoader呢？
ItemLoader 简介
通过之前的学习，已经知道网页的基本解析流程就是先通过 css/xpath 方法进行解析，然后再把值封装到 Item 中，如果有特殊需要的话还要对解析到的数据进行转换处理，这样当解析代码或者数据转换要求过多的时候，会导致代码量变得极为庞大，从而降低了可维护性。同时在 sipider 中编写过多的数据处理代码某种程度上也违背了单一职责的代码设计原则。我们需要使用一种更加简洁的方式来获取与处理网页数据，ItemLoader 就是用来完成这件事情的。
ItemLoader 类位于 scrapy.loader ，它可以接收一个 Item 实例来指定要加载的 Item, 然后指定 response 或者 selector 来确定要解析的内容，最后提供了 add_css()、 add_xpath() 方法来对通过 css 、 xpath 解析赋值，还有 add_value() 方法来单独进行赋值。 
# 不使用的情况： 
title = response.xpath('//div[@class="entry-header"]/h1/text()').extract()[0]
article_item["title"] = title
# 使用的情况： 
item_loader.add_css("title", ".entry-header h1::text")
# 至于具体的提取逻辑则在 Item.py文件中进行处理
# yield article_item则将 item传递给pipeline.py由pipeline内的类进行处理【保存至本地、数据库或者其他操作】
item.py
# 定义爬虫要爬取域的 item 模型，类似javabean，也可以使用django 的model。
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join

import datetime
import re


def return_value(value):
    # 小技巧  
    return value

class ArticelspiderItem(scrapy.Item):
    # 默认创建的item类
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
 	pass
 
def add_jobbole(self, value):
    return value + "-jobbole"
 
 
def date_convert(value):
    try:    # 可共用 提取数字
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

# 自定义item模型 用于统一处理对应类型
class JobboleArticleItem(scrapy.Item):
    # item只有一种类型 统一为Field 可以接受任何类型 类似字典形式
    # 在下面可以对输入进行预处理 
    “”“
需要说明的是：
input_processor  是对该输入进行预处理的固定参数
output_processor  是对该输出进行预处理的固定参数
    ”“”
    title = scrapy.Field(
        # 自定义对title预处理 在末尾添加标示
        # MapCompose()可以从左到右调用函数 进行处理 title 注意：MapCompose可以调用多个函数
        # input_processor = MapCompose(add_jobbole)  # 调用add_jobbole函数对title进行处理
        input_processor = MapCompose(lambda x:x + "-jobbole")  # 一种方法
    )
    create_date = scrapy.Field(
        # 预处理时间 2017/2/23 成 2017-2-23
        input_processor = MapCompose(date_convert),  # 此处相当于参数
        # output_processor = TakeFirst()
  # TakeFirst() 见名识意 即取【列表|...】第一个
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    # front_image_url必须是list 若用default_input_processor会导致下载出错
    # 覆盖掉之前的方法
    front_image_url = scrapy.Field(
        output_processor=MapCompose(return_value)  # 覆盖掉 default_input_processor
# 由于 default_input_processor对所有域都进行了默认输出处理 因此调用return_value
# 覆盖调默认输出处理
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
        # 转变后：“”
  # 转变前：['职场 程序员计算机专业']
        # 转变后：‘职场 程序员计算机专业'
        input_processor = MapCompose(remove_comment_tags),
        output_processor = Join(",")
    )
    content = scrapy.Field()


middlewares.py
scrapy中间件
Spider中间件是介入到Scrapy的spider处理机制的钩子框架，可以添加代码来处理发送给 Spiders的response及spider产生的item和request。

pipelines.py
import codecs
import json

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi   # 可以将MySQLdb的一些操作变成异步化操作

import MySQLdb
import MySQLdb.cursors
'''
利用pipeline保存到数据库中   pipelin用于处理数据域
'''
# 设置中打开ITEM_PIPELINES方可生效
class ArticelspiderPipeline(object):
# 自动生成的Pipeline
    def process_item(self, item, spider):
        return item   # 要返回item [处理后的] 因为其他类可能要用


class JsonWithEncodingPipeline(object):
    # 自定义json文件的导出
    # 打开json文件 利用codecs处理文件 可以避免编码方面的麻烦
    def __init__(self):
        self.file = codecs.open("article.json", "w", encoding="utf-8")
    def process_item(self, item, spider):
        # 处理item的关键地方
        lines = json.dumps(dict(item), ensure_ascii=False)+"\n"  # ensure_ascii=False 防止写入中文出错
        self.file.write(lines)
        # 处理完之后 要返回去 下一个pipeline可能需要处理
        return item
    def spider_closed(self, spider):
        # 重载 当spider关闭时 保存文件
        self.file.close()

class MysqlPipeline(object):
    """
    自定义将数据写入数据库
    """
    def __init__(self):
        self.conn = MySQLdb.connect(host="127.0.0.1", user="root", password="123456", db="article_spider", charset="utf8",
                                    use_unicode=True)
        self.cursor = self.conn.cursor()   # 实例化游标

    def process_item(self, item, spider):
        insert_sql = """insert into jobbole_article(title, url, create_date, fav_nums)
                        values (%s, %s, %s, %s)"""
        # 使用`占位符
        self.cursor.execute(insert_sql, (item["title"], item["url"], item["create_date"], item["fav_nums"]))
        # 用commit（）才会提交到数据库
        self.conn.commit()

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()


class MysqlTwistedPipeline(object):
    # 采用异步机制写入MySQL
    # 由于爬虫的爬取速度可能要快于数据写入数据库的速度 这样很容易造成阻塞 因此可以通过异步处理这种情况
    def __init__(self, dppool):
        self.dppool = dppool
  # 创建连接池实例
    # 用固定方法 【写法固定】  获取配置文件内信息
    @classmethod
    def from_settings(cls, settings):   # cls实际就是本类 MysqlTwistedPipeline
        dpparms = dict(
  # 从配置文件中获取参数
        host = settings["MYSQL_HOST"],
        db = settings["MYSQL_DBNAME"],
        user = settings["MYSQL_USER"],
        passwd = settings["MYSQL_PASSWORD"],
        charset = "utf8",
        cursorclass = MySQLdb.cursors.DictCursor, # 指定 curosr 类型  需要导入MySQLdb.cursors
        use_unicode = True
        )  # 由于要传递参数 所以参数名成要与connnect保持一致
        # 用的仍是MySQLdb的库 twisted并不提供
        # 异步操作
        # adbapi # 可以将MySQLdb的一些操作变成异步化操作
        dppool = adbapi.ConnectionPool("MySQLdb", **dpparms) 
       # 告诉它使用的是哪个数据库模块  连接参数  pymysql 或者 MySQLdb

        return cls(dppool)    # 即实例化一个pipeline

    def process_item(self, item, spider):
        # 使用twisted将mysql插入编程异步操作
        # 指定操作方法和操作的数据 [下面会将方法异步处理]
        query = self.dppool.runInteraction(self.do_insert, item)
        # AttributeError: 'Deferred' object has no attribute 'addErrorback'
        # query.addErrorback(self.handle_error)  # 处理异常
        query.addErrback(self.handle_error)  # 处理异常


    def handle_error(self, failure, item, spider):
        # 定义错误 处理异步插入的异常
        print(failure)


    def do_insert(self, cursor, item):
        """
        此类内其他都可以看作是通用 针对不同的sql操作只需要改写这里即可了
        :param cursor:
        :param item:
        :return:
        """
        insert_sql = """insert into jobbole_article(title, url, create_date, fav_nums, url_object_id,
                        front_image_url, front_image_path, comment_nums, praise_nums, tags, content)
                                values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )"""
        # 使用`占位符
        cursor.execute(insert_sql, (item["title"], item["url"], item["create_date"], item["fav_nums"],
                                    item["url_object_id"], item["front_image_url"],
                                    item["front_image_path"], item["comment_nums"], item["praise_nums"],
                                    item["tags"],item["content"]))


class JsonExporterPipeline(object):
    # 调用scrapy提供的json文件 exporter导出json文件
    def __init__(self):
        self.file = open("articleexporter.json", "wb")
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item




# 定义自己的pipeline用于自定义存储图片
class ArticleImagePipeline(ImagesPipeline):
    """
   设置文件保存路径
    """
    def item_completed(self, results, item, info):
        # 重载该函数
        if "front_image_url" in item:
            for ok, value in results:
                image_file_path = value["path"]
            item["front_image_path"] = image_file_path
        return item

"""
需要在自定义的ImagePipeline类中重载的方法：get_media_requests(item, info)和item_completed(results, items, info)。 
正如工作流程所示，Pipeline将从item中获取图片的URLs并下载它们，所以必须重载get_media_requests，并返回一个Request对象，这些请求对象将被Pipeline处理，当完成下载后，结果将发送到item_completed方法，这些结果为一个二元组的list，每个元祖的包含(success, image_info_or_failure)。 * success: boolean值，true表示成功下载 * image_info_or_error：如果success=true，image_info_or_error词典包含以下键值对。失败则包含一些出错信息。 * url：原始URL * path：本地存储路径 * checksum：校验码。
"""
results : <class 'list'>: [(True, {'url': 'http://jbcdn2.b0.upaiyun.com/2016/04/49961db8952e63d98b519b76a2daa5e2.png', 'checksum': 'fd1fdd2b782851c8885067ada2799a5d', 'path': 'full/c766feed221138f7946130756cddfc7e86e388b4.jpg'})]



setting.py
配置文件
# -*- coding: utf-8 -*-
import os
# Scrapy settings for ArticelSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'ArticelSpider'

SPIDER_MODULES = ['ArticelSpider.spiders']
NEWSPIDER_MODULE = 'ArticelSpider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'ArticelSpider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True  # False 防止过滤掉不符合机器爬取规则的URL
# 爬取被阻止 则更改为False
# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# 设置下载时延
# CONCURRENT_REQUESTS_PER_DOMAIN = 1
# DOWNLOAD_DELAY=2
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'ArticelSpider.middlewares.ArticelspiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'ArticelSpider.middlewares.ArticelspiderDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # 'ArticelSpider.pipelines.JsonExporterPipeline': 2,
    'scrapy.pipelines.images.ImagesPipeline':2,  # scrapy自带图片下载 数字表示处理顺序【在该列表中的处理顺序】
    'ArticelSpider.pipelines.ArticleImagePipeline': 1,  # 重载方法 获取图片保存路径
    # 'ArticelSpider.pipelines.MysqlPipeline': 1,
    'ArticelSpider.pipelines.MysqlTwistedPipeline': 3,  # 异步处理数据保存至数据库


}
# 配置item爬去字段
IMAGES_URLS_FIELD = "front_image_url"  # 需要注意的是 scrapy会将front_image_url当成数组处理 所以格式要正确
project_dir = os.path.abspath(os.path.dirname(__file__))
# 讲两个路径名链接 找到images文件
IMAGES_STORE = os.path.join(project_dir, 'images')   # 尽量配置相对路径

# 过滤掉小图片
# IMAGES_MIN_HEIGHT=100
# IMAGES_MIN_WIDTH=100

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

MYSQL_HOST = "127.0.0.1"
MYSQL_DBNAME = "article_spider"  # 数据库名称 非表名称 表名称会在sql语句中指明
MYSQL_USER = "root"
MYSQL_PASSWORD = "123456"

最后main.py文件  运行文件
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

终端运行：
maxinehehe@maxinehehe-PC:~$  scrapy crawl jobbole         
jobbole为爬虫名称 
至此项目完成。
