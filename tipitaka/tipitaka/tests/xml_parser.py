#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from scrapy.selector import Selector

class TextObject:
  def __init__(self, text):
    self.text = text
    self.url = ""

def parse_test():
    text = """<?xml version="1.0" encoding="UTF-16"?><tree>
<tree text="1. pārājikakaṇḍaṃ" action="cscd/vin01t2.tik0.xml" target="text" />
<tree text="2. saṅghādisesakaṇḍaṃ" action="cscd/vin01t2.tik1.xml" target="text" />
<tree text="3. aniyatakaṇḍaṃ" action="cscd/vin01t2.tik2.xml" target="text" />
<tree text="4. nissaggiyakaṇḍaṃ" action="cscd/vin01t2.tik3.xml" target="text" /></tree>
    """
    response = TextObject(text=text) 
    selector = Selector(response, type="xml")
    
    # use XPath selector to extract the required info
    trees = selector.xpath("/tree/tree").getall()
    for tree in trees:
        xml = Selector(text=tree, type="xml")
        text =  xml.xpath("./@text").get()
        src = xml.xpath("./@action").get()
        print('level4', text, src)


if __name__ == "__main__":
    parse_test()
