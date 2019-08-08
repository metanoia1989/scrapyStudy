#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import pymongo
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from egafd.items import ActressItem, FilmItem


class MongoPipeline(object):
    """
    将提取的数据存储到 mongodb
    """
    collection_actress = 'actress'
    collection_film = 'movie'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASER', 'egafd')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, ActressItem):
            self.db[self.collection_actress].insert_one(dict(item))
            return item

        if isinstance(item, FilmItem):
            self.db[self.collection_film].insert_one(dict(item))
            return item


class DumplicatesPipeline(object):
    def __init__(self):
        self.actress_set = set()
        self.film_set = set()

    def process_item(self, item, spider):
        if isinstance(item, ActressItem):
            name = item['name']
            if name in self.actress_set:
                raise DropItem("发现重复的演员数据：%s" % item)
            self.actress_set.add(name)
            item.cover = item.images[0]
            return item

        if isinstance(item, FilmItem):
            title = item['title']
            if title in self.film_set:
                raise DropItem("发现重复的电影数据：%s" % item)
            self.film_set.add(title)
            return item
        

class CoverPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if not item['image_url']:
            raise DropItem("Item contains no image")
        yield scrapy.Request(item['image_url'])

    def item_completed(self, results, item, info):
        logging.warning('存储结果')
        logging.warning(results)
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['cover'] = image_paths[0]
        return item