#!/usr/bin/env python
# -*- coding: utf-8 -*-
import scrapy, sys, re
from scrapy.spider import Spider#, Rule
from itjuzi.items import ItjuziItem
#from scrapy.linkextractors import LinkExtractor
from pprint import pprint

from itjuzi.settings import *


class spider(Spider):
    name = "itjuzi"
    allow_domains = [
        "www.itjuzi.com"
    ]
    start_urls = [
        "http://www.itjuzi.com/company?page=1"
    ]

    def parse(self, response):
        if response.status == 200:
            for sel in response.xpath('//p[@class="title"]/a'):
                company_url = sel.xpath('@href').extract()[0]
                yield scrapy.Request(company_url, callback=self.parse_content, dont_filter=True)

            next_page_xpath = response.xpath('//div[contains(@class, "ui-pagechange")]/a')
            for i in next_page_xpath:
                if i.xpath('text()').re(u'.*下一页.*'):
                    next_page = i.xpath('@href').extract()[0]
            if next_page:
                print "next_page: %s" % next_page
                yield scrapy.Request(next_page, callback=self.parse, dont_filter=True) #dont_filter 防止'Filtered duplicate request'错误

    def parse_content(self, response):
        if response.status == 200:
            item = ItjuziItem()
            item['itjuzi_id'] = self.charset(response.xpath('//input[@name="com_id"]/@value').extract()[0])
            item['company_name'] = self.charset(response.xpath('//input[@name="com_name"]/@value').extract()[0])
            item['company_sec_name'] = self.charset(response.xpath('//input[@name="com_sec_name"]/@value').extract()[0])
            item['company_slogan'] = self.charset(response.xpath('//input[@name="com_slogan"]/@value').extract()[0])
            yield item

    def charset(self, string):
        charset_string = ""
        if string:
            sub_field = re.sub(r',\.{3}', '', string)
            charset_string = sub_field.encode('utf8').strip()
        return string

