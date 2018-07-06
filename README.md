<<<<<<< HEAD
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

详情 参见 word 文件 ：【伯乐在线爬虫个人全面学习和理解【不断完善】.docx】

=======
基于scrapy进行爬取伯乐在线的最新文章 将每篇文章的缩略图保存至本地 异步处理爬取的数据保存至MySQL数据库。

一 。首先创建个人虚拟环境：
1.安装虚拟环境 virtualenvwrapper 【使用豆瓣源】

maxinehehe@maxinehehe-PC:~$  pip install -i https://pypi.douban.com.simple/ virtualenvwrapper

2.【windows忽略】修改bashrc文件

maxinehehe@maxinehehe-PC:~$  gedit ~/.bashrc

添加：
export WORKON_HOME=$HOME/.virtualenvs  
# .virtualenvs是虚拟环境文件夹 可自己创建

source /media/maxinehehe/5C584003583FDB0A/python35/Scripts/virtualenvwrapper.sh
# 可通过 find / -name virtualenvwrapper.sh

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

详情 参见 word 文件 ：【伯乐在线爬虫个人全面学习和理解【不断完善】.docx】
>>>>>>> 2a2f192917015d132dfc3eec1500b849592836a7
