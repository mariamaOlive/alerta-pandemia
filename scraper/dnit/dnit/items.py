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


class DnitHourItem(scrapy.Item):

    day = scrapy.Field()
    survey = scrapy.Field()
    point = scrapy.Field()
    hora = scrapy.Field()
    sentido = scrapy.Field()
    vh = scrapy.Field()
    C1 = scrapy.Field()
    C2 = scrapy.Field()
    C3 = scrapy.Field()
    C4 = scrapy.Field()
    C5 = scrapy.Field()
    M = scrapy.Field()
    O1 = scrapy.Field()
    O2 = scrapy.Field()
    O3 = scrapy.Field()
    P1 = scrapy.Field()
    P2 = scrapy.Field()
    P3 = scrapy.Field()
    R1 = scrapy.Field()
    R2 = scrapy.Field()
    R3 = scrapy.Field()
    R4 = scrapy.Field()
    R5 = scrapy.Field()
    R6 = scrapy.Field()
    S1 = scrapy.Field()
    S2 = scrapy.Field()
    S3 = scrapy.Field()
    S4 = scrapy.Field()
    S5 = scrapy.Field()
    S6 = scrapy.Field()
    SE1 = scrapy.Field()
    SE2 = scrapy.Field()
    SE3 = scrapy.Field()
    SE4 = scrapy.Field()
    SE5 = scrapy.Field()



    

 