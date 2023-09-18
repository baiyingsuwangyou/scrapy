# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from Spider import settings
import os


class SpiderPipeline(object):
    def process_item(self, item, spider):
        with open(settings.SAVE_PATH, 'a') as f:
            f.write('职位名称：' + item['job_name'] + '\n')
            f.write('公司名称：' + item['company_name'] + '\n')
            f.write('职位薪资：' + item['salary'] + '\n')
            f.write('发布时间：' + item['date'] + '\n')
            f.write('原始地址：' + item['job_link'] + '\n')
            a = item['job_info']
            a = a.replace('\xa0', '')
            a = a.replace(' ', '')
            # print(a)
            f.write('岗位职责：' + '\n' + a + '\n')
            f.write('\n')
        return item
