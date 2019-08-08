# -*- coding: utf-8 -*-
import scrapy
from egafd.items import FilmItem
from os import linesep

class FilmSpider(scrapy.Spider):
    name = 'film'
    allowed_domains = ['egafd.com']
    start_urls = ['http://egafd.com/']

    def parse(self, response):
        for href in response.css('h2')[3].xpath('.//a/@href').getall():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse_list)

    def parse_list(self, response):
        for href in response.css('.flma::attr(href)').getall():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse_film)

    def parse_film(self, response):
        item = FilmItem()

        item['title'] = response.xpath('//h1/text()').re(r'\xa0(.*?)(\xa0)?$')[0]
        item['notes']= ' '.join(response.css('.notes::text').getall())
        item['actresses']= response.css('.act::text').getall()
        item['review']= linesep.join(response.css('.act::text').getall()) 

        yield item