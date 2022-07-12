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

# title of each columns of the excel file
FIELDNAMES = ['company name', 'pv name', 'pv model', 'pv_type', 'pmax stc', 'vmax stc', 'voc stc', 'isc stc', 'imax stc', 'efficiency stc', 'tolerance', 'pmax noct',
              'vmax noct', 'voc noct', 'isc noct', 'imax noct', 'temp noct', 'temp range', 'temp pmax coef', 'temp voc coef', 'temp isc coef']


class EnfScraperPipeline(object):
    """
    a class used for writing the data to the excel file

    attributes:
    -----------
    wb: openpyxl.Workbook
        the workbook object
    ws: openpyxl.worksheet.worksheet.Worksheet
        the worksheet object

    methods:
    --------
    open_spider(self, spider):
        open the excel file
    process_item(self, item, spider):
        write the data to the excel file
    close_spider(self, spider):
        close the excel file


    """

    wb = None
    ws = None

    def open_spider(self, spider):
        """
        the method will be used  for opening the excel file and creating
        the worksheet

        parameters:
        -----------
        spider: scrapy.Spider
            the spider object be used for the pipeline to get the name
            of the excel file

        """
        self.wb = openpyxl.Workbook()
        self.ws = self.wb.active

        self.ws.append(FIELDNAMES)

    def process_item(self, item, spider):
        """ 
        the method will be used for writing the data to the excel file

        parameters:
        -----------
        item: scrapy.Item
            the item object to be used for the pipeline to get the data to be 
            written to the excel file
        """
        adapter = ItemAdapter(item)

        self.ws.append([adapter.get("company_name"),
                        adapter.get("pv_name"),
                        adapter.get("pv_model"),
                        adapter.get("pv_type"),
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
        """
        the method will be used for closing the excel file

        parameters:
        -----------
        spider: scrapy.Spider
            the spider object used by the pipeline to obtain the scraped information 
        """
        self.wb.save(XLSX_PATH)
