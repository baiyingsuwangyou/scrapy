# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    job_link = scrapy.Field()
    job_name = scrapy.Field()
    company_name = scrapy.Field()
    salary = scrapy.Field()
    date = scrapy.Field()
    job_info = scrapy.Field()
    index = scrapy.Field()
