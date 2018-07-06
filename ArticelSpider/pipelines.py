# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

"""
该文件处理要抓取的域
"""
import codecs
import json

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi   # 可以将MySQLdb的一些操作变成异步化操作

import MySQLdb
import MySQLdb.cursors
'''
利用pipeline保存到数据库中  
'''
# 设置中打开ITEM_PIPELINES方可生效
class ArticelspiderPipeline(object):
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
    def __init__(self, dppool):
        self.dppool = dppool

    # 用固定方法 【写法固定】  获取配置文件内信息
    @classmethod
    def from_settings(cls, settings):   # cls实际就是本类 MysqlTwistedPipeline
        dpparms = dict(
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
        dppool = adbapi.ConnectionPool("MySQLdb", **dpparms) # 告诉它使用的是哪个数据库模块  连接参数

        return cls(dppool)  # 即实例化一个pipeline

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
    通过在setting.py中设置 即可抓取文件
    """
    def item_completed(self, results, item, info):
        # 重载该函数
        if "front_image_url" in item:
            for ok, value in results:
                image_file_path = value["path"]

            item["front_image_path"] = image_file_path
        return item
