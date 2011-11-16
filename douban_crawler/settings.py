# Scrapy settings for douban_crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'douban_crawler'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['douban_crawler.spiders']
NEWSPIDER_MODULE = 'douban_crawler.spiders'
DEFAULT_ITEM_CLASS = 'douban_crawler.items.DoubanCrawlerItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

DOWNLOAD_DELAY = 0.6

ITEM_PIPELINES = ['douban_crawler.pipelines.DoubanCrawlerPipeline']

DB = './data/douban'

DB_CONN = None
