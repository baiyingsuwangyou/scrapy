import scrapy
import re
from scrapy_project.items import ScrapyProjectItem
from scrapy import Selector
import datetime


class FirstspiderSpider(scrapy.Spider):
    name = "firstspider"
    allowed_domains = ["rc.cqhc.cn"]
    start_urls = ["https://rc.cqhc.cn/index.php?m=work&c=list&classid=120&sort=updateline&page=1"]
    pages = 6

    def start_requests(self):
        for page in range(1, self.pages + 1):
            yield scrapy.Request(url=self.start_urls[0][:-1] + str(page), callback=self.parse)

    def parse(self, response):
        # print(response.url)
        selector = Selector(response)
        url_lists = selector.xpath('//div[1]/div[3]/div[2]/el-row/el-col/el-space/el-link/@href').extract()
        items = []
        for url in url_lists:
            item = ScrapyProjectItem()
            item['job_url'] = url
            items.append(item)

        for item in items:
            yield scrapy.Request(url=item['job_url'], meta={'item': item}, callback=self.parsed)

    def parsed(self, response):
        item = response.meta['item']
        # job_url
        item['job_url'] = response.url
        print(item['job_url'])
        selector = Selector(response)

        # job_name
        item['job_name'] = selector.xpath('//div[1]/div[2]/div/div/div[1]/h1/el-space/span/text()').extract()[0]
        # print(item['job_name'])

        # company_name
        item['company_name'] = selector.xpath('//div[1]/div[3]/div[2]/div[1]/div[2]/a/text()').extract()[0]
        # print(item['company_name'])

        # salary
        item['salary'] = selector.xpath('//div[1]/div[2]/div/div/div[1]/div/el-space/span[1]/text()').extract()[0]
        # print(item['salary'])

        # time
        time = selector.xpath('//div[1]/div[2]/div/div/div[2]/div[2]/span[1]/text()').extract()[0]
        time = time[4:]
        if '前' in time:
            now_time = datetime.datetime.now()
            if '天' in time:
                time = int(time[:-2])
                time = now_time - datetime.timedelta(days=time)
            elif '小时' in time:
                time = int(time[:-3])
                time = now_time - datetime.timedelta(hours=time)
            elif '分钟' in time:
                time = int(time[:-3])
                time = now_time - datetime.timedelta(minutes=time)
            time = time.strftime('%Y-%m-%d')
        item['time'] = time
        # print(item['time'])

        # job_mes
        text = selector.xpath('//div[1]/div[3]/div[1]/div[1]/div').extract()[0]
        text = text.replace(' ', '')
        text = text.replace('\n', '')
        text = text.replace('\r', '')
        text = re.findall('>(.*?)<', text)
        text = ''.join(text)
        text = text.replace('\xa0', '')
        text = text.replace('\u2665', '')
        text = text.replace('\u2022', '')
        item['job_mes'] = text
        print(item['job_mes'])

        yield item
