# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DnitItem(scrapy.Item):

    survey = scrapy.Field()
    point = scrapy.Field()
    day = scrapy.Field()
    date = scrapy.Field()
    crescente = scrapy.Field()
    decrescente = scrapy.Field()
    total = scrapy.Field()


class DnitVehicleItem(scrapy.Item):

    survey = scrapy.Field()
    point = scrapy.Field()
    classe = scrapy.Field()
    total = scrapy.Field()
    percentage = scrapy.Field()

 