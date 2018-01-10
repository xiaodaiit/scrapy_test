# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs  #这个模块是编码转换
import json
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item

class JsonJobbolepiderPipeline(object):
    #保存为json文件
    def __init__(self):
        self.file = codecs.open('article.json','w',encoding="utf-8")

    def process_item(self, item, spider):
        lines = json.dumps(dict(item),ensure_ascii=False) + "\n"
       # json.dumps 序列化时对中文默认使用的ascii编码.想输出真正的中文需要指定ensure_ascii = False
        self.file.write(lines)
        return item

    def spider_closed(self,spider):
        self.file.close()

class MysqlJobbolepiderPipeline(object):
    #采用同步的机制写入mysql
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1','root','root','ebt',charset="utf8",use_unicode=True) #use_unicode 使用编码
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql,params = item.get_insert_sql()
        # 执行sql语句
        self.cursor.execute(insert_sql,params)



class MysqlTwistedPipline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool)


    def process_item(self, item, spider):
    #异步插入数据库
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)

    def handle_error(self, failure, item, spider):
        print(failure)

    def do_insert(self, cursor, item):
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)










