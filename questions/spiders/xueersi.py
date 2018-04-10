# -*- coding: utf-8 -*-
import scrapy
import time
import numpy
import re
from questions.items import QuestionsItem


class xueersiSpider(scrapy.Spider):
    name = "xueersi"
    allowed_domains = ["tiku.xueersi.com"]
    start_urls = [
        "http://tiku.xueersi.com/shiti/list_1_1_0_0_4_0_1",
        "http://tiku.xueersi.com/shiti/list_1_2_0_0_4_0_1",
        "http://tiku.xueersi.com/shiti/list_1_3_0_0_4_0_1",
    ]
    levels = ['偏易','中档','偏难']
    subjects = ['英语','语文','数学']
    count = 0
    # def start_requests(self):
    #     yield scrapy.Request('http://tiku.xueersi.com/shiti/5717',callback=self.getanswer)
    def parse(self, response):
        arr = response.xpath("//ul[@class='pagination']/li/a/text()").extract()
        total_page = arr[3]
        for index in range(int(total_page)):
            yield scrapy.Request(response.url.replace('_0_0_4_0_1',"_0_0_4_0_"+str(index)),callback=self.getquestion)
            
    def getquestion(self,response):
        self.count = self.count+1
        for res in response.xpath('//div[@class="main-wrap"]/ul[@class="items"]/li'):
            item = QuestionsItem()
            # 获取问题
            questions = res.xpath('./div[@class="content-area"]').re(r'<div class="content-area">?([\s\S]+?)<(table|\/td|div|br)')
            if len(questions):
                # 获取题目
                question = questions[0].strip()
                item['source'] = question
                dr = re.compile(r'<[^>]+>',re.S)
                question = dr.sub('',question)
                content = res.extract()
                item['content'] = question
                # 获取课目
                subject =  re.findall(ur'http:\/\/tiku\.xueersi\.com\/shiti\/list_1_(\d+)',response.url)
                item['subject'] = self.subjects[int(subject[0])-1]
                # 获取难度等级
                levels = res.xpath('//div[@class="info"]').re(ur'难度：([\s\S]+?)<')
                item['level'] = self.levels.index(levels[0])+1
                
                # 获取选项
                options =  re.findall(ur'[A-D]\.([\s\S]+?)<(\/td|\/p|br)',content)
                item['options'] = options
                if len(options):
                    url = res.xpath('./div[@class="info"]/a/@href').extract()[0]
                    request = scrapy.Request(url,callback=self.getanswer)
                    request.meta['item'] = item
                    yield request
            #for option in options:
                
    def getanswer(self,response):
        
        res = response.xpath('//div[@class="part"]').re(ur'<td>([\s\S]+?)<\/td>')
        con = re.findall(ur'([\s\S]+?)<br>[\s\S]+?([A-D])',res[0])
        if con:
            answer = con[0][1]
            analysis = con[0][0]
        else:
            answer = res[0]
            analysis = ''
        if answer:
            item = response.meta['item']
            item['answer'] = answer.strip()
            item['analysis'] = analysis.strip()
            yield item
        
        
        
        

        
