# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import json


class XpathValidatorPipeline:
    def open_spider(self, spider):
        self.file = open('error_urls.json', 'w', encoding='utf-8')
        self.items = []

    def close_spider(self, spider):
        json.dump(self.items, self.file, ensure_ascii=False, indent=4)
        self.file.close()

    def process_item(self, item, spider):
        self.items.append(dict(item))
        return item


