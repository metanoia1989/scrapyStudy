# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import scrapy
from scrapy.exceptions import DropItem
from nfcmag.items import CategoryItem, ArticleItem

class NfcmagPipeline(object):
    def process_item(self, item, spider):
        return item

class MongoPipeline(object):
    """
    将提取的数据存储到 mongodb
    """
    collection_article = 'article'
    collection_category = 'category'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASER', 'nfcmag')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, ArticleItem):
            article = self.db[self.collection_article].find_one({'title': item['title']})
            if article is not None:
                raise DropItem("发现重复的文章数据：%s" % item)
            category_name = item.pop('category_name', None)
            category = self.db[self.collection_category].find_one({'name': category_name})
            item['category_id'] = category.get('_id') if category is not None else None
            self.db[self.collection_article].insert_one(dict(item))
            return item

        if isinstance(item, CategoryItem):
            self.db[self.collection_category].insert_one(dict(item))
            return item
        