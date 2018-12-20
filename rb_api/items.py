# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RbApiItem(scrapy.Item):
    # define the fields for your item here like:
    disciplina = scrapy.Field()
    av1 = scrapy.Field()
    av2 = scrapy.Field()
    exame = scrapy.Field()
    media = scrapy.Field()
    resultado = scrapy.Field()
    
