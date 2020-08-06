# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DouBanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    auth = scrapy.Field()
    translator = scrapy.Field()
    publisher = scrapy.Field()
    date = scrapy.Field()
    price = scrapy.Field()
    rating = scrapy.Field()
    hot = scrapy.Field()
    url = scrapy.Field()
