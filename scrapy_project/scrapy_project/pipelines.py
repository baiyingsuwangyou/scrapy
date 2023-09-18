# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy_project import settings


class ScrapyProjectPipeline:
    def process_item(self, item, spider):
        with open('./job.txt', 'a') as f:
            f.write('职位名称：' + item['job_name'] + '\n')
            f.write('公司名称：' + item['company_name'] + '\n')
            f.write('职位薪资：' + item['salary'] + '\n')
            f.write('发布时间：' + item['time'] + '\n')
            f.write('原始地址：' + item['job_url'] + '\n')
            f.write('岗位职责：' + item['job_mes'] + '\n')
            f.write('\n')
        return item
