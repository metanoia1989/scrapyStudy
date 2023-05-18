# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.exceptions import DropItem
from itemadapter import ItemAdapter
import psycopg
from psycopg.rows import dict_row 
from . import config
from .items import ChapterItem, ChapterContentItem


class MySQLStorePipeline:
    def __init__(self) -> None:
        self.connection = psycopg.connect(config.POSTGRES_URI, row_factory=dict_row)
        self.cursor = self.connection.cursor()

    def open_spider(self, spider):
        self.items = []

    def close_spider(self, spider):
        # Sort the items based on the sorting_order field:
        sorted_items = sorted(self.items, key=lambda item: (
            item.get('level', 0),  
            item.get('parent_order', 0),  
            item.get('sort_order', 1)
        ))

        # Process the sorted items
        for item in sorted_items:
            if isinstance(item, ChapterItem):
                self.process_chapter(item, spider)

        self.cursor.close()
        self.connection.close()

    def process_item(self, item, spider):
        """
        item处理分发器
        """
        # 章节item优先分类，最后处理
        if isinstance(item, ChapterItem):
            self.items.append(item)

        # 章节内容，直接处理 
        if isinstance(item, ChapterContentItem):
            self.process_content(item, spider)

        return item
   
    def process_chapter(self, item, spider):
        """
        插入章节数据
        """
        try:
            # 查询父级
            parent_name = item.get("parent_name_pali") # 竟然为None 奇怪 
            self.cursor.execute("select * from chapters where name_pali = %s", [parent_name])
            parent = self.cursor.fetchone()
            
            if parent is not None:
                parent_id = parent.get("id")
                level = parent.get("level") + 1
            else:
                parent_id = 0
                level = 1

            # 查询是否已存在此章节 
            name_pali = item.get("name_pali")
            self.cursor.execute("select * from chapters where name_pali = %s and pid = %s", [name_pali, parent_id])
            current = self.cursor.fetchone()

            if current is not None:
                raise DropItem("Duplicate item found: %s" % item)

            # 插入操作 
            item_data = [
                parent_id,
                level,
                item.get("url"),
                item.get("name_pali"),
            ]
            self.cursor.execute("INSERT INTO chapters (pid, level, url, name_pali)" 
                                "VALUES (%s, %s, %s, %s)", item_data)

            self.connection.commit()
        except DropItem as e:
            return item
        except Exception as e:
            self.connection.rollback()
            print('exception', e)
            raise e


    def process_content(self, item, spider):
        """
        插入章节内容
        """
        try:
            # 重复检测处理  
            chapter_id = item.get('chapter_id')
            self.cursor.execute("select * from chapter_content where chapter_id = %s", [chapter_id])
            current = self.cursor.fetchone()
            if current is not None:
                raise DropItem("Duplicate item found: %s" % item)

            item_data = [
                chapter_id,
                item.get("html")
            ]
            self.cursor.execute("INSERT INTO chapter_content (chapter_id, html) VALUES (%s, %s)", item_data)

            self.connection.commit()

        except DropItem as e:
            return item
        except Exception as e:
            self.connection.rollback()
            print('exception', e)
            raise e
