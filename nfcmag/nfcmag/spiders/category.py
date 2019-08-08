# -*- coding: utf-8 -*-
import scrapy
from nfcmag.items import CategoryItem

class CategorySpider(scrapy.Spider):
    name = 'category'
    allowed_domains = ['www.nfcmag.com']
    start_urls = ['https://www.nfcmag.com/category/10.html']

    def parse(self, response):
        categores = response.css('.categoryListSub').xpath('./following-sibling::a/text()').getall()
        for category in categores:
            item = CategoryItem(name=category)
            yield item
            
