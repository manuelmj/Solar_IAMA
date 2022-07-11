# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy import signals
from scrapy import Request

from ENF_scraper.items import EnfScraperItem

from itemadapter import ItemAdapter

import openpyxl

from ENF_scraper.settings import XLSX_PATH

FIELDNAMES = ['company name', 'pv name','pv model', 'pmax stc', 'vmax stc', 'voc stc', 'isc stc', 'imax stc', 'efficiency stc', 'tolerance', 'pmax noct',
              'vmax noct', 'voc noct', 'isc noct', 'imax noct', 'temp noct', 'temp range', 'temp pmax coef', 'temp voc coef', 'temp isc coef']


class EnfScraperPipeline(object):
    wb = None
    ws = None

    def open_spider(self, spider):
        self.wb = openpyxl.Workbook()
        self.ws = self.wb.active

        self.ws.append(FIELDNAMES)

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        self.ws.append([adapter.get("company_name"),
                        adapter.get("pv_name"),
                        adapter.get("pv_model"),
                        adapter.get("pmax_stc"), 
                        adapter.get("vmax_stc"), 
                        adapter.get("voc_stc"), 
                        adapter.get("isc_stc"), 
                        adapter.get("imax_stc"), 
                        adapter.get("efficiency_stc"), 
                        adapter.get("tolerance"), 
                        adapter.get("pmax_noct"), 
                        adapter.get("vmax_noct"), 
                        adapter.get("voc_noct"), 
                        adapter.get("isc_noct"), 
                        adapter.get("imax_noct"), 
                        adapter.get("temp_noct"), 
                        adapter.get("temp_range"), 
                        adapter.get("temp_pmax_coef"), 
                        adapter.get("temp_voc_coef"), 
                        adapter.get("temp_isc_coef")])
        return item

    def close_spider(self, spider):
        self.wb.save(XLSX_PATH)
