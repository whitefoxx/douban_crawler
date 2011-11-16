# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class GroupUserItem(Item):
    # define the fields for your item here like:
    # name = Field()
    group = Field()
    homepage = Field()
    name = Field()
    image = Field()

    def __str__(self):
        return 'GroupUserItem(homepage: %s)' % self['homepage']

class UserMovieItem(Item):
    user = Field()
    subject = Field()
    rating = Field()
    date = Field()
    tags = Field()
    comment = Field()

    def __str__(self):
        return 'UserMovieItem(subject: %s)' % self['subject']
