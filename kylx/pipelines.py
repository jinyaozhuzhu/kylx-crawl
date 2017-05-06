# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

from . import settings


class HukePipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()
        self.select_sql = "SELECT url FROM kylx WHERE url='{url}'"

        self.insert_sql = "INSERT INTO kylx (url,content,start_date,start_milli,title,school)"\
                          "VALUES ('{url}','{content}','{start_date}','{start_milli}','{title}','{school}')"
        self.school = "华中科技大学"

    def process_item(self, item, spider):
        self.cursor.execute(self.select_sql.format(url=item['url']))
        result = self.cursor.fetchone()
        if result is None:
            try:
                self.cursor.execute(
                    self.insert_sql.format(url=item['url'],
                                           content=item['content'],
                                           start_date=item['start_date'],
                                           start_milli=item['start_milli'],
                                           title=item['title'],
                                           school=self.school)
                )
                self.connect.commit()
                print("保存成功")
            except Exception as e:
                print("保存出错！", e.__str__())
        else:
            print("已经存在！")
        return item


class WudaPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()
        self.select_sql = "SELECT url FROM kylx WHERE url='{url}'"

        self.insert_sql = "INSERT INTO kylx (url,content,end_date,end_milli,title,school)"\
                          "VALUES ('{url}','{content}','{end_date}','{end_milli}','{title}','{school}')"
        self.school = "武汉大学"

    def process_item(self, item, spider):
        self.cursor.execute(self.select_sql.format(url=item['url']))
        result = self.cursor.fetchone()
        if result is None:
            try:
                self.cursor.execute(
                    self.insert_sql.format(url=item['url'],
                                           content=item['content'],
                                           start_date=item['end_date'],
                                           start_milli=item['end_milli'],
                                           title=item['title'],
                                           school=self.school)
                )
                self.connect.commit()
                print("保存成功")
            except Exception as e:
                print("保存出错！", e.__str__())
        else:
            print("已经存在！")
        return item
