# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
from csv import DictWriter


def item_type(item):
    return type(item).__name__.lower()


def item_fields(item):
    return item.fields.keys()


class MultiCsvPipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            output_dir=crawler.settings.get('VOTES_CSV_OUTPUT_DIR'),
            encoding=crawler.settings.get('VOTES_CSV_ENCODING'),
            csv_params={
                'delimiter': crawler.settings.get('VOTES_CSV_DELIMITER')
            }
        )

    def __init__(self, output_dir, encoding, csv_params=None):
        if csv_params is None:
            csv_params = {}

        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        self.encoding = encoding

        self.csv_params = csv_params

        self.output = None
        self.spider_count = 0

    def process_item(self, item, spider):
        item_name = item_type(item)
        fields = item_fields(item)

        if item_name not in self.output:
            f = open(os.path.join(self.output_dir, item_name + '.csv'), 'wb')
            w = DictWriter(f, fields, **self.csv_params)
            w.writeheader()
            self.output[item_name] = (f, w)

        res = {nom: (field.encode(self.encoding) if isinstance(field, unicode) else field)
               for nom, field in item.iteritems()}
        self.output[item_name][1].writerow(res)

    def open_spider(self, spider):
        self.spider_count += 1
        if self.output is None:
            self.output = {}

    def close_spider(self, spider):
        self.spider_count -= 1

        if self.spider_count == 0:
            for file, _ in self.output.values():
                file.close()

            self.output = None
