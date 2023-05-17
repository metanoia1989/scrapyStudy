import scrapy


class ChapterSpider(scrapy.Spider):
    """
    抓取章节结构     
    """
    name = 'chapter'
    allowed_domains = ['tipitaka.org']
    start_urls = ['http://tipitaka.org/romn/']

    def parse(self, response):
        pass
