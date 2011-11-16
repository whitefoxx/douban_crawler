#encoding=utf-8

from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.contrib.loader import XPathItemLoader
from scrapy.http import Request
import re
import sqlite3

from douban_crawler.items import UserMovieItem
from douban_crawler.dbmanager import DBManager

class UserMovieSpider(BaseSpider):
    name = "userMovie"
    allowed_domains = ["douban.com"]
    dbmg = DBManager()
    start_urls = dbmg.get_start_urls("user_movie")
	
    def parse(self, response):
        url = response.url
        user = url[url.find('people'):].split('/')[1]
        #which = url.split('/')[-1] if url[-1] != '/' else url.split('/')[-2]
        hxs = HtmlXPathSelector(response)

        dls = hxs.select('//div[@class="item"]/div[@class="info"]/ul')
        items = []
        for dl in dls:
            item = UserMovieItem()
            subject = dl.select('li[@class="title"]/a/@href').extract()[0]
            subject = subject.split('/')[-2] if subject[-1] == '/' else\
                    subject.split('/')[-1]
            rating = dl.select('li[3]/span[1]/@class').extract()
            date = dl.select('li[3]/span[@class="date"]/text()').extract()
            tags = dl.select('li[3]/span[@class="tags"]/text()').extract()
            comment = dl.select('li[4]/text()').extract()

            rating = int(rating[0][6]) if len(rating) > 0 and len(rating[0]) > 6 else -1
            date = date[0] if len(date) > 0 else ''
            tags = tags[0].split(':')[1] if len(tags) > 0 else ''
            comment = comment[0] if len(comment) > 0 else ''
             
            l = XPathItemLoader(item=item, selector=dl)
            l.add_value('user', user)
            l.add_value('subject', subject)
            l.add_value('rating', rating)
            l.add_value('date', date)
            l.add_value('tags', tags)
            l.add_value('comment', comment)
            yield l.load_item()

        links = hxs.select('//span[@class="next"]/a/@href').extract()
        for url in links:
            print url
            yield Request(url, callback=self.parse)
        if len(links) < 1:
            p = re.compile('<span class="next">.*?<a href="(.+?)">',re.S)
            m = p.search(response.body_as_unicode())
            if m:
                url = m.group(1)
                print url
                yield Request(url, callback=self.parse)
            else:
                url = self.dbmg.more_url('user_movie')
                if url:
                    print url
                    yield Request(url, callback=self.parse)


