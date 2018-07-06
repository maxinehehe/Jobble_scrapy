# -*- coding: utf-8 -*-
import scrapy, re
from scrapy import Request
from scrapy.loader import ItemLoader
from urllib import parse  # python2 import urlparse

from ArticelSpider.items import JobboleArticleItem, ArticleItemLoader
from ArticelSpider.utils.common import get_md5
import datetime

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    # 允许域名
    allowed_domains = ['blog.jobbole.com']
    # 起始URL
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        """
        # 改写parse
        1. 获取文章列表页中的文章url并交给scrapy下载后并进行解析
        2. 获取下一页的URL病并交给scrapy进行下载， 下载完成后交给parse
        :param response:
        :return:
        """

        # 解析列表页中的所有文章URL 拿到当前页文章的网址列表数组
        # post_urls = response.xpath('//*[@id="archive"]/div[@class="post floated-thumb"]/div[@class="post-thumb"]/a/@href').extract()
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")  # 获取节点

        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first("")  # extract()[0]
            post_url = post_node.css("::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url":image_url}, callback=self.parse_detail)
            # 当域名 并不存在 如 110287 【http://blog.jobbole.com】 + /110287
            # 只能处理域名 url=parse.urljoin(response.url, post_url)
            # python 提供了包 方法 来解决上述问题
            # Request(url=parse.urljoin(response.url, post_url), callback=self.parse_detail)  # Request下载完成之后 调取函数
            # 只是初始化了Requset 那怎样进行下载呢 直接加yield
        # 提取下一页并交给scrapy进行下载
        # 下面是xpath和css两种选择器的取法
        # next_url = response.xpath('//*[@id="archive"]/div[@class="navigation margin-20"]/a[@class="next page-numbers"]/@href').extract()[0]
        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        print("下一页："+next_url+"\n")
        if next_url:
            # 拿到下一页 交给scrapy下载器
            # yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse) # 传函数名即可 由底层twisted调用
            # 错误原因 由于传递的是post_url始终转回爬取这一页 而next_url并未传递过去
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)  # 传函数名即可 由底层twisted调用


    def parse_detail(self, response):
        """
        提取文章的具体字段
        :param response:
        :return:
        """
        # 编写数据的解析和爬取
        article_item = JobboleArticleItem() # 实例化


        # title = response.xpath('//div[@class="entry-header"]/h1/text()').extract()[0]
        # create_date = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract()[0].strip().replace("·", "").strip()
        # # 用/text()获取值
        # # 另外对于xpath id定位较为准确
        # # 返回的是SelectorList[] 可以继续做选择
        # praise_nums = response.xpath("//span[contains(@class, 'vote-post-up')]/h10/text()").extract()[0]
        # fav_nums = response.xpath("//span[contains(@class, 'bookmark-btn')]/text()").extract()[0]
        # match_re = re.match(".*?(\d+).*", fav_nums)
        # if match_re:
        #     fav_nums = int(match_re.group(1))
        # else:
        #     fav_nums = 0
        #
        # comment_nums = response.xpath("//a[@href='#article-comment']/span/text()").extract()[0]
        # match_re = re.match(".*?(\d+).*", comment_nums)
        # if match_re:
        #     comment_nums = int(match_re.group(1))
        # else:
        #     comment_nums = 0
        # content = response.xpath("//div[@class='entry']").extract()[0]
        #
        # tag_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        # tag_list = [element for element in tag_list if not element.endswith("评论")]
        # tags = "".join(tag_list)
        #
        # article_item["url_object_id"] = get_md5(response.url)
        # article_item["title"] = title
        # article_item["url"] = response.url
        # try:
        #     create_date = datetime.datetime.strptime(create_date, "%y/%m/%d").date()
        # except Exception as e:
        #     create_date = datetime.datetime.now()
        # article_item["create_date"] = create_date
        # article_item["front_image_url"] = [front_image_url]  # 设置中要求当成数组处理
        # article_item["praise_nums"] = praise_nums
        # article_item["comment_nums"] = comment_nums
        # article_item["fav_nums"] = fav_nums
        # article_item["tags"] = tags
        # article_item["content"] = content

        front_image_url = response.meta.get("front_image_url", "")  # 第二个“”是默认值   文章封面图
        # 通过item_loader加载item
        # 传递 实例化对象
        # ArticleItemLoader
        item_loader = ArticleItemLoader(item=JobboleArticleItem(), response=response)
        # item_loader.add_xpath("title", '//div[@class="entry-header"]/h1/text()')
        # item_loader.add_value('url', response.url)
        # item_loader.add_value('url_object_id', get_md5(response.url))
        # item_loader.add_value("front_image_url", [front_image_url])
        # item_loader.add_css("create_date", "p.entry-meta-hide-on-mobile::text")
        # # item_loader.add_xpath("create_date", "//p[@class='entry-meta-hide-on-mobile']/text()")
        # item_loader.add_css("praise_nums", ".vote-post-up h10::text")
        # item_loader.add_xpath("comment_nums", '//a[@href="#article-comment"]/span/text()')
        # item_loader.add_xpath("fav_nums", "//span[contains(@class, 'bookmark-btn')]/text()")
        # item_loader.add_xpath("tags", "//p[@class='entry-meta-hide-on-mobile']/a/text()")
        # item_loader.add_css("content", "div.entry")

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

        yield article_item   # 会传送到pipelines
