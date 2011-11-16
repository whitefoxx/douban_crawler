# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from douban_crawler.dbmanager import DBManager

class DoubanCrawlerPipeline(object):
    def __init__(self):
        self.dbmg = None
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_opened(self, spider):
        self.dbmg = DBManager()
        self.dbmg.open_db()

    def spider_closed(self, spider):
        self.dbmg.close_db()
        self.dbmg = None

    def process_item(self, item, spider):
        self.dbmg.store_item(item)
        return item

