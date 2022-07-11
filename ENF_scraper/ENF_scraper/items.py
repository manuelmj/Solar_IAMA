# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EnfScraperItem(scrapy.Item):

    # basic infomtion
    company_name = scrapy.Field()
    pv_name = scrapy.Field()
    pv_model = scrapy.Field()
    pv_type= scrapy.Field()

   # electrical features in stc (standard test conditions )
    pmax_stc = scrapy.Field()
    vmax_stc = scrapy.Field()
    voc_stc = scrapy.Field()
    isc_stc = scrapy.Field()
    imax_stc = scrapy.Field()
    efficiency_stc = scrapy.Field()
    tolerance = scrapy.Field()

   # electrical features in NOCT (nominal operating cell temperature)
    pmax_noct = scrapy.Field()
    vmax_noct = scrapy.Field()
    voc_noct = scrapy.Field()
    isc_noct = scrapy.Field()
    imax_noct = scrapy.Field()
    temp_noct = scrapy.Field()

    # thermal features
    temp_range = scrapy.Field()
    temp_pmax_coef = scrapy.Field()
    temp_voc_coef = scrapy.Field()
    temp_isc_coef = scrapy.Field()
