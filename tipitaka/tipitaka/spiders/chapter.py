import scrapy
from scrapy.selector import Selector
from tipitaka.items import ChapterItem, ChapterContentItem

class ChapterSpider(scrapy.Spider):
    """
    抓取章节结构     
    """
    name = 'chapter'
    allowed_domains = ['tipitaka.org']
    start_urls = ['https://tipitaka.org/romn/tipitaka_toc.xml']
    base_url = 'https://tipitaka.org/romn/'

    def parse(self, response):
        trees = response.xpath("/tree/tree").getall()
        i = 0
        for tree in trees:
            i = i + 1
            xml = Selector(text=tree, type="xml")
            text =  xml.xpath("./@text").get()
            src = xml.xpath("./@src").get()
            src = self.base_url + src.lstrip("./") if src else ""

            parent_name = response.meta.get("parent_name", None)
            level = 1

            yield ChapterItem(name_pali=text, url=src, parent_name_pali=parent_name, 
                              level=level, sort_order=i, parent_order=0)

            if len(src) > 0:
                yield scrapy.Request(src, 
                    callback=self.parse_level2, 
                    priority = level,
                    meta={
                        'parent_name': text, 
                        'level': level + 1,
                        'parent_order': i,
                    }
                )

    def parse_level2(self, response):
        level2_trees = response.xpath("/tree/tree").getall()
        i = 0
        for level2_tree in level2_trees:
            i = i + 1
            xml = Selector(text=level2_tree, type="xml")
            text =  xml.xpath("./@text").get()
            parent_name = response.meta.get("parent_name", None)
            level = response.meta.get("level", 2)
            parent_order = response.meta.get("parent_order", 0)

            yield ChapterItem(name_pali=text, url="", parent_name_pali=parent_name, 
                              level=level, sort_order=i, parent_order=parent_order)
            for item in self.parse_level3(level2_tree, text, level+1, parent_order=i):
                yield item

    def parse_level3(self, response, parent_name, level, parent_order):
        response = Selector(text=response, type="xml")
        trees = response.xpath("./tree").getall()
        i = 0
        for tree in trees:
            i = i + 1
            xml = Selector(text=tree, type="xml")
            text =  xml.xpath("./@text").get()
            src = xml.xpath("./@src").get()
            src = self.base_url + src.lstrip("./") if src else ""

            yield ChapterItem(name_pali=text, url=src, parent_name_pali=parent_name, 
                            level=level, sort_order=i, parent_order=parent_order)

            if len(src) > 0:
                yield scrapy.Request(src, 
                    callback=self.parse_level4, 
                    priority = level,
                    meta={
                        'parent_name': text, 
                        'level': level + 1,
                        'parent_order': i,
                    }
                )
    
    def parse_level4(self, response):
        trees = response.xpath("/tree/tree").getall()
        i = 0
        for tree in trees:
            i = i + 1
            xml = Selector(text=tree, type="xml")
            text =  xml.xpath("./@text").get()
            src = xml.xpath("./@action").get()
            src = self.base_url + src.lstrip("./") if src else ""

            parent_name = response.meta.get("parent_name", None)
            level = response.meta.get("level", 4)
            parent_order = response.meta.get("parent_order", 0)

            yield ChapterItem(name_pali=text, url=src, parent_name_pali=parent_name, 
                              level=level, sort_order=i, parent_order=parent_order)

            # if len(src) > 0:
            #     yield scrapy.Request(src, 
            #         callback=self.parse_content, 
            #         priority = level,
            #         meta={
            #             'parent_name': text, 
            #             'level': level + 1,
            #         }
            #     )

    def parse_content(self, response):
        pass 

