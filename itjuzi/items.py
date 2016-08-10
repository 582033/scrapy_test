# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ItjuziItem(scrapy.Item):
    itjuzi_id = scrapy.Field()
    company_name = scrapy.Field()
    company_sec_name = scrapy.Field()
    company_slogan = scrapy.Field()
