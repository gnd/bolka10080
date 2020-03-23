# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# create table jokes(id int(11) primary key auto_increment, domain varchar(255), url varchar(255), joke blob);
import os
import sys
import MySQLdb
import ConfigParser
reload(sys)
sys.setdefaultencoding('utf-8')

class Bolka10080Pipeline(object):
    def __init__(self):
        ### load config
        settings_file = os.path.join(sys.path[-1], 'bolka10080/settings_python')
        config = ConfigParser.ConfigParser()
        config.readfp(open(settings_file))
        self.dbhost = config.get('database', 'DB_HOST')
        self.dbuser = config.get('database', 'DB_USER')
        self.dbpass = config.get('database', 'DB_PASS')
        self.dbname = config.get('database', 'DB_NAME')
        self.dbtable = config.get('database', 'DB_TABLE')

    def open_spider(self, spider):
        self.db = MySQLdb.connect(host=self.dbhost, user=self.dbuser, passwd=self.dbpass, db=self.dbname)
        self.cur = self.db.cursor()

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        query = "INSERT INTO %s (domain, url, joke) VALUES('%s', '%s', '%s')" % (self.dbtable, item["domain"], item["url"], item["joke"])
        self.cur.execute(query)
        self.db.commit()
        return item
