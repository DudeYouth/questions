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

    def parse(self, response):
        arr = response.xpath("//ul[@class='pagination']/li/a/text()").extract()
        total_page = arr[2]
        for index in numpy.arange(1,int(total_page),1):
            yield scrapy.Request(response.url.replace('_0_0_4_0_1"',"_0_0_4_0_"+str(index)),callback=self.getquestion)
            
    def getquestion(self,response):
        for res in response.xpath('//div[@class="content-area"]'):
            questions = res.re(r'<(\/span|td)>([\s\S]+?)<(table|\/td)>')
            question = questions[1]
            content = res.extract()
            options =  re.findall(r'[A-D]\.([\s\S]+?)<(\/td|\/p|br)',content)
            for option in options:
                

        
        
        
        

        
