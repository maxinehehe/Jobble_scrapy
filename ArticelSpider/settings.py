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