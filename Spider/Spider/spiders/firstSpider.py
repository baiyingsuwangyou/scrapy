import scrapy
import re
from Spider.items import SpiderItem
from scrapy import Selector
import datetime
import time


class FirstspiderSpider(scrapy.Spider):
    name = 'firstSpider'
    allowed_domains = ['www.flrcw.com']
    # 'https://www.flrcw.com/job/?c=search&keyword={python}&minsalary=&maxsalary='
    start_urls = ['https://www.flrcw.com/job/list/6_36-0-0-0_0_0_0_0_0_0_0-0-0-0-1.html']
    # 'https://www.flrcw.com/job/list/0-0-0-0_0_0_0_0_0_0_0-0-0-0-2.html?%E5%B7%A5%E7%A8%8B%E5%B8%88'
    # 'https://www.flrcw.com/job/list/6-0-0-0_0_0_0_0_0_0_0-0-0-0-1.html'

    pages = 4

    def start_requests(self):
        for page in range(1, self.pages + 1):
            yield scrapy.Request(url=self.start_urls[0][:-6] + str(page) + '.html', callback=self.parse)

    def parse(self, response):
        # print(response.url)
        selector = Selector(response)
        urls_lists = selector.xpath('//div[4]/div/div[5]/div/div')
        items = []
        for res in urls_lists[:-2]:
            url = res.xpath('./div[1]/div[1]/a/@href').extract()[0]
            # print(url)
            item = SpiderItem()
            item['job_link'] = url
            items.append(item)

        for item in items:
            yield scrapy.Request(url=item['job_link'], meta={'item': item}, callback=self.parse_detail)

    def parse_detail(self, response):
        item = response.meta['item']
        item['job_link'] = response.url
        selector = Selector(response)
        item['job_name'] = selector.xpath('//div[6]/div/div[2]/div[1]/h1/text()').extract()[0]
        item['company_name'] = selector.xpath('//div[8]/div[2]/div[1]/div[2]/a/text()').extract()[0]
        item['salary'] = selector.xpath('//div[6]/div/div[2]/div[1]/span/text()').extract()[0]
        date_str = \
            selector.xpath('//div[6]/div/div[2]/div[1]/div[@class="job_details_topright_data"]/span/text()').extract()[
                0][
            :-4]
        if '前' in date_str:
            date = int(date_str[:-3])
            now = datetime.datetime.now()
            if '分钟' in date_str:
                date = datetime.timedelta(minutes=date) + now
            elif '小时' in date_str:
                date = datetime.timedelta(hours=date) + now
            date_str = date.strftime('%Y-%m-%d')
        # print(date_str)
        item['date'] = date_str
        print(item['job_link'])

        # div[3]/span[@class="job_details_describe_yq"]
        job_info = '。'.join(
            selector.xpath(
                '//div[8]/div[1]/div[1]/div[3]/span[@class="job_details_describe_yq"]/text()').extract()) + '。'

        # div[3]/div
        lists = []
        for sel in selector.xpath('//div[8]/div[1]/div[1]/div[3]/div[1]/span'):
            lists.append(sel.xpath('./text()').extract()[0])
        if len(lists) != 0:
            job_info += '语言要求：' + '，'.join(lists) + '。'

        # div[3]/text()
        a = selector.xpath('//div[8]/div[1]/div[1]/div[3]/text()').extract()
        a = [i for i in a if '\t' not in i]
        a = '。'.join(a)
        job_info += a + '。'

        # div[3]/p
        a = ''.join(selector.xpath('//div[8]/div[1]/div[1]/div[3]/p').extract())
        a = re.findall('>(.*?)<', a)
        a = [i for i in a if i != '']
        a = ''.join(a)
        job_info += a

        item['job_info'] = job_info

        yield item
