# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class QuestionsPipeline(object):
    def __init__(self):  
        # connection database  
        self.connect = pymysql.connect('localhost','root','','question',use_unicode=True,charset='utf8')  
        # get cursor  
        self.cursor = self.connect.cursor()  
        print("connecting mysql success!")  
        self.answer = ['A','B','C','D']
    def process_item(self, item, spider):
        sqlstr = "insert into question(content,subject,level,answer,analysis) VALUES('%s','%s','%s','%s','%s')"%(pymysql.escape_string(item['content']),item['subject'],item['level'],item['answer'],pymysql.escape_string(item['analysis']))
        self.cursor.execute(sqlstr)
        for index in  range(len(item['options'])):
            option = item['options'][index]
            answer = self.answer.index(item['answer'])
            if answer==index:
                ans = '2'
            else:
                ans = '1'
            sqlstr = "insert into options(content,qid,answer) VALUES('%s','%s','%s')"%(pymysql.escape_string(option[0]),self.cursor.lastrowid,ans)
            self.cursor.execute(sqlstr)
        self.connect.commit() 
        #self.connect.close() 
        return item
