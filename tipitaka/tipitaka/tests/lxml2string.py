#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from lxml import etree
import lxml

text = """<?xml version="1.0" encoding="UTF-16"?><tree>
<tree text="1. pārājikakaṇḍaṃ" action="cscd/vin01t2.tik0.xml" target="text" />
<tree text="2. saṅghādisesakaṇḍaṃ" action="cscd/vin01t2.tik1.xml" target="text" />
<tree text="3. aniyatakaṇḍaṃ" action="cscd/vin01t2.tik2.xml" target="text" />
<tree text="4. nissaggiyakaṇḍaṃ" action="cscd/vin01t2.tik3.xml" target="text" /></tree>
"""

trees = etree.fromstring(text.encode('utf-16')).xpath("/tree/tree")

for tree in trees:
    print(etree.tostring(tree, pretty_print=True).decode("utf-8"))