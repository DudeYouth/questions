# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QuestionsItem(scrapy.Item):
    content = scrapy.Field()
    subject = scrapy.Field()
    level = scrapy.Field()
    answer = scrapy.Field()
    options = scrapy.Field()
    analysis = scrapy.Field()
    source = scrapy.Field()
    answer_url = scrapy.Field()
    pass
