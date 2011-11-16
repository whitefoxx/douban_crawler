#encoding=utf-8

from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.contrib.loader import XPathItemLoader
from scrapy.http import Request
import re

from douban_crawler.items import GroupUserItem
from douban_crawler.init import get_start_urls

class GroupSpider(BaseSpider):
    name = "group"
    allowed_domains = ["douban.com"]
    start_urls = get_start_urls("group_user")
	
    def parse(self, response):
        url = response.url
        group_name = url[url.find('group'):].split('/')[1]
        hxs = HtmlXPathSelector(response)

        dls = hxs.select('//dl[@class="obu"]')
        items = []
        for dl in dls:
            item = GroupUserItem()
            l = XPathItemLoader(item=item, selector=dl)
            l.add_xpath('homepage', 'dt/a/@href')
            l.add_xpath('image', 'dt/a/img/@src')
            l.add_xpath('name', 'dd/a/text()')
            l.add_value('group', group_name)
            yield l.load_item()

        links = hxs.select('//span[@class="next"]/a/@href').extract()
        for url in links:
            yield Request(url, callback=self.parse)
        if len(links) < 1:
            p = re.compile('<span class="next">.*?<a href="(.+?)">',re.S)
            m = p.search(response.body_as_unicode())
            if m:
                url = m.group(1)
                yield Request(url, callback=self.parse)

