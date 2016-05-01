# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BronzeMirrorItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    name = scrapy.Field()
    size = scrapy.Field()
    desc = scrapy.Field()
    create_age = scrapy.Field()
    valuation = scrapy.Field()
    deal = scrapy.Field()
    auction_company = scrapy.Field()
    auction_date = scrapy.Field()
    auction_meet = scrapy.Field()
    auction_session = scrapy.Field()
    url = scrapy.Field()
    file_urls = scrapy.Field()
