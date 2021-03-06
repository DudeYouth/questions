# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import md5


class QuestionsPipeline(object):
    def __init__(self):  
        # connection database  
        self.connect = pymysql.connect('localhost','root','','question',use_unicode=True,charset='utf8')  
        # get cursor  
        self.cursor = self.connect.cursor()  
        print("connecting mysql success!")  
        self.answer = ['A','B','C','D']
    def process_item(self, item, spider):
        content = pymysql.escape_string(item['content'])
        m1 = md5.new()   
        m1.update(content)
        hash = m1.hexdigest()
        selectstr = "select id from question where hash='%s'"%(hash)
        self.cursor.execute(selectstr)
        res = self.cursor.fetchone()
        if not res:
            sqlstr = "insert into question(content,source,subject,level,answer,analysis,hash,answer_url) VALUES('%s','%s','%s','%s','%s','%s','%s','%s')"%(content,pymysql.escape_string(item['source']),item['subject'],item['level'],item['answer'],pymysql.escape_string(item['analysis']),hash,item['answer_url'])
            self.cursor.execute(sqlstr)
            qid = self.cursor.lastrowid
            for index in  range(len(item['options'])):
                option = item['options'][index]
                answer = self.answer.index(item['answer'])
                if answer==index:
                    ans = '2'
                else:
                    ans = '1'
                sqlstr = "insert into options(content,qid,answer) VALUES('%s','%s','%s')"%(pymysql.escape_string(option[0]),qid,ans)
                self.cursor.execute(sqlstr)
            self.connect.commit() 
            #self.connect.close() 
        return item
