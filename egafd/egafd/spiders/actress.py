# -*- coding: utf-8 -*-
import scrapy
from egafd.items import ActressItem

class ActressSpider(scrapy.Spider):
    name = 'actress'
    allowed_domains = ['egafd.com']
    start_urls = ['http://egafd.com/']

    def parse(self, response):
        for href in response.css('h2')[1].xpath('.//a/@href').getall():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse_list)

    def parse_list(self, response):
        for href in response.css('.acta::attr(href)').getall():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parse_actress)

    def parse_actress(self, response):
        item = ActressItem()

        names = response.xpath('//h1/text()').re(r'\xa0(.*?).?(\[\d\])?$')
        item['name'] = names[0] if names[1] == '' else names[0] + ' ' + names[1] 
        item['notes']= response.xpath('//tr[@class="hdr"]/th[contains(text(),"Notes")]') \
            .xpath('../following-sibling::tr[1]//li/text()').get()
        item['cover'] =  item['image_url']  = \
            response.urljoin(response.xpath('//div[@align="center"]/img/@src').get()) 
        item['films']= []
        for film_selector in response.xpath('//tr[@class="hdr"]/th[contains(text(),"Films")]') \
            .xpath('../following-sibling::tr[1]//li'):
            film = film_selector.xpath('./descendant::*/text()[1]').get() 
            item['films'].append(film)

        yield item