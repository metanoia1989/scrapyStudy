import scrapy
from scrapy.selector import Selector
from tipitaka.items import ChapterItem
from tipitaka.common import get_first
from lxml import etree

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
        doc = etree.fromstring(response.text.encode("utf-16"))
        level2_trees = doc.xpath("/tree/tree")

        i = 0
        for xml in level2_trees:
            i = i + 1
            text =  xml.xpath("./@text")[0]
            parent_name = response.meta.get("parent_name", None)
            level = response.meta.get("level", 2)
            parent_order = response.meta.get("parent_order", 0)

            print('level2', text)
            # print('level2 html', parent_name, etree.tostring(xml, encoding="unicode", pretty_print=True))

            yield ChapterItem(name_pali=text, url="", parent_name_pali=parent_name, 
                              level=level, sort_order=i, parent_order=parent_order)
            for item in self.parse_level3(xml, text, level+1, parent_order=i):
                yield item

    def parse_level3(self, response, parent_name, level, parent_order):
        trees = response.xpath("./tree")
        i = 0

        for xml in trees:
            i = i + 1
            text =  xml.xpath("./@text")[0] 
            src = get_first(xml.xpath("./@src")) 
            src = self.base_url + src.lstrip("./") if src else ""

            print('level3', text, src)
            # print('level3 html', parent_name, etree.tostring(xml, encoding="unicode", pretty_print=True))

            yield ChapterItem(name_pali=text, url=src, parent_name_pali=parent_name, 
                            level=level, sort_order=i, parent_order=parent_order)

            # 对经集进行特别处理    
            if text == "Dīgha nikāya (aṭṭhakathā)":
                print(text, etree.tostring(xml, encoding="unicode", pretty_print=True))
            children = xml.xpath('./tree')
            if children and len(children):
                j = 0
                for child in children: 
                    j = j + 1
                    c_text =  child.xpath("./@text")[0] 
                    c_src = get_first(child.xpath("./@src")) 
                    c_src = self.base_url + c_src.lstrip("./") if c_src else ""

                    print('level3-special', c_text, c_src)

                    yield ChapterItem(name_pali=c_text, url=c_src, parent_name_pali=text, 
                                    level=level+1, sort_order=j, parent_order=i)

                    yield scrapy.Request(c_src, 
                        callback=self.parse_level4, 
                        priority = level + 1,
                        meta={
                            'parent_name': c_text, 
                            'level': level + 2,
                            'parent_order': j,
                        }
                    )
            

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
        parent_name = response.meta.get("parent_name", None)
        level = response.meta.get("level", 4)
        parent_order = response.meta.get("parent_order", 0)

        trees = etree.fromstring(response.text.encode('utf-16')).xpath("/tree/tree")

        i = 0
        for xml in trees:
            i = i + 1
            text =  xml.xpath("./@text")[0]
            src = get_first(xml.xpath("./@action")) 
            src = self.base_url + src.lstrip("./") if src else ""
            print('level' + str(level), text, src)

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

