# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ChapterItem(scrapy.Item):
    # define the fields for your item here like:
    pid = scrapy.Field()
    level = scrapy.Field()
    url = scrapy.Field()
    name_pali = scrapy.Field()

class ChapterContentItem(scrapy.Item):
    # define the fields for your item here like:
    chapter_id = scrapy.Field()
    html = scrapy.Field()
