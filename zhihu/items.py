# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class Answer(scrapy.Item):
    # define the fields for your item here like:
     title = scrapy.Field()
    #指纹 
     finger = scrapy.Field()
    #赞的数量
     count = scrapy.Field()
    # answer url
     url = scrapy.Field()
