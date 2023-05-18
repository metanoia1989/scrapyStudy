#!/usr/bin/env python3
#-*- coding: utf-8 -*-

"""
公开的对象和方法 
"""

class TextObject:
  def __init__(self, text, url):
    self.text = text
    self.url = url


def get_first(list):
  if hasattr(list, '__len__') and len(list) > 0:
    return list[0] 
  else:
    return None
