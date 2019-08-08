# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy



class CategoryItem(scrapy.Item):
    name = scrapy.Field()

class ArticleItem(scrapy.Item):
    title = scrapy.Field() # 标题
    period = scrapy.Field() # 第几期
    introduction = scrapy.Field() # 简介
    author = scrapy.Field() # 作者
    source = scrapy.Field() # 来源
    date = scrapy.Field() # 日期
    category_id = scrapy.Field() # 分类ID
    category_name = scrapy.Field() # 分类名
    content = scrapy.Field() # 内容

class LinkItem(scrapy.Item):
    url = scrapy.Field()