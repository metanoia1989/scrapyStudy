# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.exceptions import DropItem
from itemadapter import ItemAdapter
import psycopg
import config
from items import ChapterItem, ChapterContentItem


class MySQLStorePipeline:
    def __init__(self) -> None:
        self.connection = psycopg.connect(config.POSTGRES_URI)
        self.cursor = self.connection.cursor()

    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()

    def process_item(self, item, spider):
        """
        item处理分发器
        """
        if isinstance(item, ChapterItem):
            return self.process_chapter(self, item, spider)

        if isinstance(item, ChapterContentItem):
            return self.process_content(self, item, spider)

        return item
    
    def process_chapter(self, item, spider):
        """
        插入章节数据
        """
        try:
            # 查询是否已存在此章节 
            name_pali = item.get("name_pali")
            self.cursor.execute("select * from chapters where name_pali = %s", name_pali)
            current = self.cursor.fetchone()
            if current is not None:
                raise DropItem("Duplicate item found: %s" % item)

            # 查询父级
            parent_name = item.get("parent_name_pali"),
            self.cursor.execute("select * from chapters where name_pali = %s", parent_name)
            parent = self.cursor.fetchone()
            if parent is not None:
                parent_id = parent.get("id")
                level = parent.get("level") + 1
            else:
                parent_id = 0
                level = 1

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
        except Exception as e:
            self.connection.rollback()
            raise e

    def process_content(self, item, spider):
        """
        插入章节内容
        """
        try:
            # 重复检测处理  
            chapter_id = item.get('chapter_id')
            self.cursor.execute("select * from chapter_content where chatper_id = %s", chapter_id)
            current = self.cursor.fetchone()
            if current is not None:
                raise DropItem("Duplicate item found: %s" % item)

            item_data = [
                chapter_id,
                item.get("html")
            ]
            self.cursor.execute("INSERT INTO chapter_content (chatper_id, html) VALUES (%s, %s)", item_data)
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise e
