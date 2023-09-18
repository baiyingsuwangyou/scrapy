# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyProjectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    job_url = scrapy.Field()
    job_name = scrapy.Field()
    job_mes = scrapy.Field()
    company_name = scrapy.Field()
    salary = scrapy.Field()
    time = scrapy.Field()
