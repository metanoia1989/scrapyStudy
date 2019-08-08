# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from nfcmag.items import ArticleItem
from functools import reduce


class ArticleSpider(CrawlSpider):
    name = 'article'
    allowed_domains = ['www.nfcmag.com']
    start_urls = ['https://www.nfcmag.com/category/10.html']
    rules = [
        Rule(LinkExtractor(restrict_css='.first>a', allow=(r'category')), 
            callback='parse_list', process_links='process_links'),
        Rule(LinkExtractor(restrict_css='.next>a', allow=(r'category')), 
            callback='parse_list', process_links='process_links', follow=True),
    ]

    def parse_start_url(self, response):
        """提取所有分类链接"""
        links = LinkExtractor(restrict_css='.category-box li>a') \
            .extract_links(response)
        urls = [link.url for link in links]
        for url in urls:
            yield scrapy.Request(url)
    
    def process_links(self, links):
        for link in links:
            print('最终的链接 ：%s' % str(link))
            yield link

    def parse_list(self, response):
        links = LinkExtractor(restrict_css='.article-items h5>a') \
            .extract_links(response)
        urls = [link.url for link in links]
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_article)

    def parse_article(self, response):
        get_intro = lambda prev, next: prev if (len(prev) > len(next)) else next
        intro = response.css('.intro ::text').getall()

        item = ArticleItem()
        item['title'] = response.css('.subject::text').get()
        item['introduction'] = reduce(get_intro, intro) if len(intro) > 0 else ''
        item['content'] = ''.join( response.css('.content ::text').getall())
        info = list(map(lambda text: text.split('：').pop(), response.css('.author::text').getall()))
        if len(info) == 2:
            [item['source'], item['date']] = info
        elif len(info) == 1:
            item['date'] = info.pop()
        else:
            [item['author'], item['source'], item['date']] = info
        [_, item['period'], item['category_name']] = response.css('.breadcrumbs a::text').getall()
        yield item

        