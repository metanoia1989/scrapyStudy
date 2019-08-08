# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ActressItem(scrapy.Item):
    name = scrapy.Field()  # 姓名
    notes = scrapy.Field()  # 说明
    films = scrapy.Field()  # 电影
    cover = scrapy.Field()  # 封面
    image_url = scrapy.Field() 

class FilmItem(scrapy.Item):
    title = scrapy.Field()  # 影片名
    notes = scrapy.Field()  # 说明
    actresses = scrapy.Field() # 演员
    review = scrapy.Field() # 描述