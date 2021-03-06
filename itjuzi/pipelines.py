# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json, MySQLdb
from pprint import pprint


class ItjuziPipeline(object):
    def __init__(self):
        self.db_host = 'localhost'
        self.db_username = 'root'
        self.db_passwd = ''
        self.db_database = 'itjuzi'
        self.db_charset = 'utf8'

    def process_item(self, item, spider):
        conn = MySQLdb.connect(host=self.db_host, user=self.db_username, passwd=self.db_passwd, db=self.db_database, charset=self.db_charset)
        cursor = conn.cursor()

        itjuzi_id = item['itjuzi_id']
        company_name = item['company_name'] or ""
        company_sec_name = item['company_sec_name'] or ""
        company_slogan = item['company_slogan'] or ""
        if self.check_juzi_id(itjuzi_id) > 0:
            #如果id已存在则更新
            sql = "update company set company_name='%s', company_sec_name='%s', company_slogan='%s' where juzi_id=%s"
            cursor.execute(sql % (company_name, company_sec_name, company_slogan, itjuzi_id))
        else:
            sql = "insert into company (juzi_id, company_name, company_sec_name, company_slogan)values(%s, %s, %s, %s)"
            #不要使用%拼接字符串,会导致sql注入及因为编码问题插入失败
            cursor.execute(sql, (itjuzi_id, company_name, company_sec_name, company_slogan))
        conn.commit()
        conn.close()

        return item


    def check_juzi_id(self, juzi_id):
        conn = MySQLdb.connect(host=self.db_host, user=self.db_username, passwd=self.db_passwd, db=self.db_database, charset=self.db_charset)
        cursor = conn.cursor()
        sql = "select id from company where juzi_id = %s"
        count = cursor.execute(sql, [juzi_id])
        conn.close()
        return count
