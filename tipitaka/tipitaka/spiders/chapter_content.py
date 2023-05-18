import scrapy

from tipitaka.db_query import db_query
from tipitaka.items import ChapterContentItem
import json
class ChapterContentSpider(scrapy.Spider):
    """
    处理章节内容 
    """
    name = "chapter_content"
    allowed_domains = ["tipitaka.org"]
    # start_urls = ["https://tipitaka.org/romn/"]

    def start_requests(self):
        db = db_query()
        chapters = db.queryAll("SELECT * FROM chapters WHERE url NOT LIKE %s and url <> ''", ['%toc%'])
        db.close()
        i = 0
        print(chapters)
        for chapter in chapters:
            chapter_id = chapter.get("id")
            url = chapter.get("url")
            i = i + 1
            print('wu', i, chapter_id, url)
            yield scrapy.Request(url, 
                callback=self.parse, 
                meta={
                    'chapter_id': chapter_id,
                }
            )

    def parse(self, response):
        chapter_id = response.meta.get("chapter_id", None)
        if chapter_id is None:
            return

        html = response.text
        yield ChapterContentItem(chapter_id=chapter_id, html=html)


