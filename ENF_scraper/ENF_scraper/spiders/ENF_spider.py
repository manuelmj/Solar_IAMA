# jul/7/2022
# this project scrapes the Enfsolar website to download information of
# the photovoltaic panels available in Colombia, in order to do a research
# work with data collection.
# The code was developed by: Alexander Arroyo Granados and Manuel Manjarres Rivera
#


import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from ENF_scraper.items import EnfScraperItem


class ENF_spider(CrawlSpider):
    """
    A classs used to scrape the data from the ENF website.

    Attributes:
    -----------
    name: str
        The name of the spider.
    allowed_domains: list
        The domains that the spider is allowed to crawl.
    start_urls: list
        The urls that the spider will start crawling from.
    xpath: str
        The xpath used to extract the panel links.
    enf_item: EnfScraperItem
        The item that will be used to store the scraped data.
    rules: list
        The rules that the spider will follow.

    methods:
    --------
    parse(self, response):
        The method that will be used to parse the data.
    data_pre_normalizer(self, data_lst: list) -> list:  
        The method that will be used to pre-normalize the data.
    is_empty_none(self, len_lst: int, data_lst: list) -> None:
        The method that will be used to check if the data is empty and set it to None.
    set_stc_noct(self, stc_noct: list) -> list:
        The method that will be used to set the STC and NOCT values.
    tempt_verifier(self, len_lst: int, data_lst: list) -> dict:
        The method that will be used to verify if the data is a temperature parameter.

    """

    name = "enfsolar"
    allowed_domains = ['es.enfsolar.com']
    start_urls = [
        'https://es.enfsolar.com/jinko-solar',
        'https://es.enfsolar.com/yingli-green-energy',
        'https://es.enfsolar.com/kyocera',
        'https://es.enfsolar.com/suntech-power',
        'https://es.enfsolar.com/csi-solar',
        'https://es.enfsolar.com/ja-solar',
        'https://es.enfsolar.com/inti-solar-3',
        'https://es.enfsolar.com/risen-energy',
        'https://es.enfsolar.com/znshine-solar',
        'https://es.enfsolar.com/jinko-solar',
        'https://es.enfsolar.com/osda-solar',
        'https://es.enfsolar.com/longi-solar-1-2-1-2',
        'https://es.enfsolar.com/solartech-power',
        'https://es.enfsolar.com/renesola',
        'https://es.enfsolar.com/gclsi',
        'https://es.enfsolar.com/sharp',
        'https://es.enfsolar.com/lg-electronics-1-2',
        'https://es.enfsolar.com/csun',
        'https://es.enfsolar.com/ae-solar',
        'https://es.enfsolar.com/luxen-solar',
        'https://es.enfsolar.com/restar-solar-energy',
        'https://es.enfsolar.com/trina-solar-1',
        'https://es.enfsolar.com/wwmusa-amerisolar',
        'https://es.enfsolar.com/hyundai-energy-solutions'
    ]
    xpath = '//li[contains(@class,"clearfix")]/a'
    enf_item = EnfScraperItem()

    rules = {
        Rule(LinkExtractor(allow=(), restrict_xpaths=(xpath)),
             callback="parse_item", follow=False)
    }

    def data_pre_normalizer(self, data_lst: list) -> list:
        """
        The method that will be used to pre-normalize the data.
        this method remove the empty values,new line characters
        and return the clean list.

        Parameters:
        -----------
        data_lst: list
            the list that will be normalized and cleaned.
            generally contain void values and new line characters
        returns:
        --------
        data_lst: list
            The pre-normalized data.
        """
        data_lst = list(map(lambda x: x.strip(), data_lst))
        data_lst = [x for x in data_lst if x]
        return data_lst

    def is_empty_none(self, len_lst: int, data_lst: list) -> None:
        """
        This method  will be used to check if the list  is empty and 
        set it to a list of None values.

        Parameters:
        -----------
        len_lst: int
            The length of the data list.
        data_lst: list
            The data that will be checked
        """
        if not data_lst:
            data_lst = [None for x in range(len_lst)]
        return data_lst

    def set_stc_noct(self, stc_noct: list) -> list:
        """
        checks if the list contains both stc and noct values or if it contains
        only stc values. 
        then the values will be separated into two lists.

        Parameters:
        -----------
        stc_noct: list
            list that contain the values of ntc and noct.
        returns:
        --------
        aux_stc:list
            list that contains stc values. 
        aux_noct: list
            list that contains noct values.
        """
        if stc_noct.count(stc_noct[0]) > 1:
            aux_stc = stc_noct[1:len(stc_noct)//2]
            aux_noct = stc_noct[(len(stc_noct)//2)+1:]
        else:
            # in case of the list contains only values of stc, the noct values will be set to None
            aux_stc = stc_noct[1:]
            aux_noct = [None for x in range(len(aux_stc))]
        return aux_stc, aux_noct

    def tempt_verifier(self, len_lst: int, data_lst: list) -> dict:
        """
        This method will be used to verify if the data is a valid 
        temperature parameter, in the contrary case, the value will
        be replaced for none. 
        the all values will be return it like a list itself value at the same value

        Parameters:
        -----------
        len_lst: int
            The length of the data list.
        data_lst: list
            The data that will be checked.

        returns:
        --------
        data_lst: dict
            dictionary of list that contain values of thermal features.
        """

        temp_parameters = ("Temperatura", "Rango de Temperatura", "Coeficiente de Temperatura de Pmax",
                           "Coeficiente de Temperatura de Voc", "Coeficiente de Temperatura de Isc")
        temp_parameters_dict = dict()
        for parameter in temp_parameters:
            if parameter in data_lst:
                temp_parameters_dict[parameter] = [
                    data_lst[data_lst.index(parameter)+1] for x in range(len_lst)]
            else:
                temp_parameters_dict[parameter] = [
                    None for x in range(len_lst)]
        return temp_parameters_dict

    def parse_item(self, response):

        # extracting the stc and noct values
        pmax_stc_noct = self.data_pre_normalizer(response.xpath(
            '//*[@id="product_info"]/div[1]/table/tbody/tr[contains(th,"(Pmax)")]/descendant::*/text()').getall())
        vmax_stc_noct = self.data_pre_normalizer(response.xpath(
            '//*[@id="product_info"]/div[1]/table/tbody/tr[contains(th,"(Vmax)")]/descendant::*/text()').getall())
        voc_stc_noct = self.data_pre_normalizer(response.xpath(
            '//*[@id="product_info"]/div[1]/table/tbody/tr[contains(th,"(Voc)")]/descendant::*/text()').getall())
        isc_stc_noct = self.data_pre_normalizer(response.xpath(
            '//*[@id="product_info"]/div[1]/table/tbody/tr[contains(th,"(Isc)")]/descendant::*/text()').getall())
        imax_stc_noct = self.data_pre_normalizer(response.xpath(
            '//*[@id="product_info"]/div[1]/table/tbody/tr[contains(th,"(Imax)")]/descendant::*/text()').getall())

        # separating the stc and noct values
        pmax_stc, pmax_noct = self.set_stc_noct(pmax_stc_noct)
        vmax_stc, vmax_noct = self.set_stc_noct(vmax_stc_noct)
        voc_stc, voc_noct = self.set_stc_noct(voc_stc_noct)
        isc_stc, isc_noct = self.set_stc_noct(isc_stc_noct)
        imax_stc, imax_noct = self.set_stc_noct(imax_stc_noct)

        # extracting the efficiency  and tolerance values
        efficiency_stc = self.data_pre_normalizer(response.xpath(
            '//*[@id="product_info"]/div[1]/table/tbody/tr[contains(th,"Eficiencia")]/descendant::*/text()').getall())
        efficiency_stc = self.is_empty_none(len(pmax_stc), efficiency_stc[1:])
        tolerance = self.data_pre_normalizer(response.xpath(
            '//*[@id="product_info"]/div[1]/table/tbody/tr[contains(th,"(+)")]/descendant::*/text()').getall())
        tolerance = self.is_empty_none(len(pmax_stc), tolerance[1:])

        # Extracting basic information about the PV
        basic_information = self.data_pre_normalizer(
            response.css('title::text').get().split('|'))
        company_name = [basic_information[0] for x in range(len(pmax_stc))]
        pv_name = [basic_information[1] for x in range(len(pmax_stc))]
        pv_model = self.data_pre_normalizer(response.xpath(
            '//*[@id="product_info"]/div[1]/table/tbody/tr[contains(th,"No.")]/descendant::*/text()').getall())
        pv_model = pv_model[1:]
        pv_type = self.data_pre_normalizer(response.xpath(
            '//td[contains(@class,"yellow")]/text()').getall())
        pv_type = [pv_type[0] for x in range(len(pmax_stc))]
        # Extracting thermal features
        thermal_features = self.data_pre_normalizer(response.xpath(
            '//*[@id="product_info"]/div[1]/table/tbody/tr[contains(th,"Temperatura")]/descendant::*/text()').getall())
        thermal_features_dict = self.tempt_verifier(
            len(pmax_stc), thermal_features)

        # optaining the rows that contain the data
        rows = zip(
            company_name,
            pv_name,
            pv_model,
            pv_type,
            pmax_stc,
            vmax_stc,
            voc_stc,
            isc_stc,
            imax_stc,
            efficiency_stc,
            tolerance,
            pmax_noct,
            vmax_noct,
            voc_noct,
            isc_noct,
            imax_noct,
            thermal_features_dict["Temperatura"],
            thermal_features_dict["Rango de Temperatura"],
            thermal_features_dict["Coeficiente de Temperatura de Pmax"],
            thermal_features_dict["Coeficiente de Temperatura de Voc"],
            thermal_features_dict["Coeficiente de Temperatura de Isc"])

        list_fields = [
            'company_name',
            'pv_name',
            'pv_model',
            'pv_type',
            'pmax_stc',
            'vmax_stc',
            'voc_stc',
            'isc_stc',
            'imax_stc',
            'efficiency_stc',
            'tolerance',
            'pmax_noct',
            'vmax_noct',
            'voc_noct',
            'isc_noct',
            'imax_noct',
            'temp_noct',
            'temp_range',
            'temp_pmax_coef',
            'temp_voc_coef',
            'temp_isc_coef']

        for row in rows:

            self.enf_item = {
                key: row[list_fields.index(key)] for key in list_fields}

            yield self.enf_item
