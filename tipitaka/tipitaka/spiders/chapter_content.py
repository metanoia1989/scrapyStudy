import scrapy


class ChapterContentSpider(scrapy.Spider):
    """
    处理章节内容 
    """
    name = "chapter_content"
    allowed_domains = ["tipitaka.org"]
    start_urls = ["https://tipitaka.org/romn/"]

    def parse(self, response):
        pass
