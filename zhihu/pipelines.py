# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy import signals
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, select,update
from zhihu.misc.log import *
import json
import codecs
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class ZhihuPipeline(object):
    #进行落地操作



    def __init__(self):
        self.result = codecs.open("fac_result", 'a', encoding='utf-8')


       # engine = create_engine("mysql://root:root@localhost:3306/zhihu?charset=utf8",encoding="utf-8", echo=True)
       # metadata = MetaData()
       # answer = Table('answer', metadata,
       #     Column('id', Integer, primary_key=True),
       #     Column('finger', String(256)),
       #     Column('title', String(256)),
       #     Column('count', Integer),
       #     Column('url', String(256)),
       # );


       #metadata.create_all(engine)
       #self.conn = engine.connect()

    def process_item(self, item, spider):
        #info("item to db:"+ item['title'])
        content = item['title'] + " " + item['url'] + "\n"
        self.result.write(content)
        self.result.flush()
        return item
