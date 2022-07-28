# CrawlSpider

## ***Table of contents***
- [X] 1. [**Spider**](https://github.com/manuelmj/Solar_IAMA/blob/main/ENF_scraper/README_CRAWLSPIDER.md#spiders)
- [X] 2. [**Items**](https://github.com/manuelmj/Solar_IAMA/blob/main/ENF_scraper/README_CRAWLSPIDER.md#Items)
- [X] 3. [**Pipelines**](https://github.com/manuelmj/Solar_IAMA/blob/main/ENF_scraper/README_CRAWLSPIDER.md#Pipelines)
- [X] 4. [**Settings**](https://github.com/manuelmj/Solar_IAMA/blob/main/ENF_scraper/README_CRAWLSPIDER.md#Settings)
- [X] 5. [***Results***](https://github.com/manuelmj/Solar_IAMA/blob/main/ENF_scraper/README_CRAWLSPIDER.md#Results)
## ***Abstrac***
This is a crawlSpider in charge of scraping [_ENFsolar_](https://es.enfsolar.com), this bot downloads information of photovoltaic panels, and reorganizes the data in data structures, for this we use more than 20 links of manufacturer's pages that contain information of their panels as data in _STC_, _NOCT_ and _THERMAL CHARACTERISTICS_ conditions, these three categories contain relevant information for this research.

## ***Spiders***

The spider works as follows, first the links and the domain to follow are defined. [***click here to view code***](https://github.com/manuelmj/Solar_IAMA/blob/main/ENF_scraper/ENF_scraper/spiders/ENF_spider.py)
```
50  name = "the spider name"
51  allowed_domains = ['the dominian to follow']
52  start_urls = [the list of links ]
```
Secondly, the spider rules are defined, in this case, the spider goes into the links and extracts all the links from the panels of each of the manufacturers. [***click here to view code***](https://github.com/manuelmj/Solar_IAMA/blob/main/ENF_scraper/ENF_scraper/spiders/ENF_spider.py)
```
81    rules = {
82        Rule(LinkExtractor(allow=(), restrict_xpaths=(xpath)),
83             callback="parse_item", follow=False)
84    }
```

The ***parse_items*** method extracts all the necessary data from the links, using the xpath expressions to extract the information from each location within the html or css. [***click here to view code***](https://github.com/manuelmj/Solar_IAMA/blob/main/ENF_scraper/ENF_scraper/spiders/ENF_spider.py)
```
182     # extracting the stc and noct values
183        pmax_stc_noct = self.data_pre_normalizer(response.xpath(
184            '//*[@id="product_info"]/div[1]/table/tbody/tr[contains(th,"(Pmax)")]/descendant::*/text()').getall())
185        vmax_stc_noct = self.data_pre_normalizer(response.xpath(
186            '//*[@id="product_info"]/div[1]/table/tbody/tr[contains(th,"(Vmax)")]/descendant::*/text()').getall())
187        voc_stc_noct = self.data_pre_normalizer(response.xpath(
188            '//*[@id="product_info"]/div[1]/table/tbody/tr[contains(th,"(Voc)")]/descendant::*/text()').getall())
199        isc_stc_noct = self.data_pre_normalizer(response.xpath(
190            '//*[@id="product_info"]/div[1]/table/tbody/tr[contains(th,"(Isc)")]/descendant::*/text()').getall())
191        imax_stc_noct = self.data_pre_normalizer(response.xpath(
192            '//*[@id="product_info"]/div[1]/table/tbody/tr[contains(th,"(Imax)")]/descendant::*/text()').getall())

201       # extracting the efficiency  and tolerance values
202        efficiency_stc = self.data_pre_normalizer(response.xpath(
203            '//*[@id="product_info"]/div[1]/table/tbody/tr[contains(th,"Eficiencia")]/descendant::*/text()').getall())
204        efficiency_stc = self.is_empty_none(len(pmax_stc), efficiency_stc[1:])
205        tolerance = self.data_pre_normalizer(response.xpath(
206            '//*[@id="product_info"]/div[1]/table/tbody/tr[contains(th,"(+)")]/descendant::*/text()').getall())
207        tolerance = self.is_empty_none(len(pmax_stc), tolerance[1:])
208
209        # Extracting basic information about the PV
210        basic_information = self.data_pre_normalizer(
211            response.css('title::text').get().split('|'))
212        company_name = [basic_information[0] for x in range(len(pmax_stc))]
213        pv_name = [basic_information[1] for x in range(len(pmax_stc))]
214        pv_model = self.data_pre_normalizer(response.xpath(
215            '//*[@id="product_info"]/div[1]/table/tbody/tr[contains(th,"No.")]/descendant::*/text()').getall())
216        pv_model = pv_model[1:]
217        pv_type = self.data_pre_normalizer(response.xpath(
218            '//td[contains(@class,"yellow")]/text()').getall())
219        pv_type = [pv_type[0] for x in range(len(pmax_stc))]
220        # Extracting thermal features
221        thermal_features = self.data_pre_normalizer(response.xpath(
222            '//*[@id="product_info"]/div[1]/table/tbody/tr[contains(th,"Temperatura")]/descendant::*/text()').getall())
223        thermal_features_dict = self.tempt_verifier(
224            len(pmax_stc), thermal_features)


```
Once the data is xtracted and normalized, we use the [***zip()***](https://www.google.com/search?client=opera&q=the+functions+zip+in+python&sourceid=opera&ie=UTF-8&oe=UTF-8) function to assemble the rows.
then we yield to each of the items 
```
227 rows = zip(
228            company_name,
229            pv_name,
230            pv_model,
231           pv_type,
232            pmax_stc,
233            vmax_stc,
234            voc_stc,
235            isc_stc,
236            imax_stc,
237            efficiency_stc,
238            tolerance,
239            pmax_noct,
240            vmax_noct,
241            voc_noct,
242            isc_noct,
243            imax_noct,
244            thermal_features_dict["Temperatura"],
245            thermal_features_dict["Rango de Temperatura"],
246            thermal_features_dict["Coeficiente de Temperatura de Pmax"],
247            thermal_features_dict["Coeficiente de Temperatura de Voc"],
248            thermal_features_dict["Coeficiente de Temperatura de Isc"])

------------------------------------------------------------------------------------


275           self.enf_item = {
276                key: row[list_fields.index(key)] for key in list_fields}
278
278            yield self.enf_item
```




## ***Items***
The elements necessary for the structuring of the data are found in this section, divided into four categories containing data on STC and NOCT conditions, thermal characteristics and basic information on the photovoltaic panel[^1]. [***click here to view code***](https://github.com/manuelmj/Solar_IAMA/blob/main/ENF_scraper/ENF_scraper/items.py)
|***basic information***| ***standard test conditions***| ***nominal operating cell temperature*** |***Thermal Ratings*** |
| :---|              :---|                    :--- |                              :--- |   
|company name|      maximun power|              maximun power|                    operating temperature range|
|panel name |       voltage at maximum power|   voltage at maximun power|         temperature coefficient of Pmax |
|panel model |      current at maximun power|   current at maximun power|         temperature coefficient of Voc  |
|tecnology |        open circuit voltage|       open circuit voltage|             temperature coefficient of Isc  |
||                  short circuit current |     short circuit current|
||                  panel efficiency|           temperature|
||                  power tolerance|
## ***Pipelines***
This pipeline stores the data in an excel file structured as follows[^2] : 

|company name |pv name|pv model|pv_type|pmax stc|vmax stc|voc stc|isc stc|imax stc|efficiency stc|tolerance|pmax noct|vmax noct|voc noct|isc noct|imax noct|temp noct|temp range|temp pmax coef|temp voc coef|temp isc coef|
| :---|:---:|:---:| :---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---:|

[***click here to view code***](https://github.com/manuelmj/Solar_IAMA/blob/main/ENF_scraper/ENF_scraper/pipelines.py)

## ***Settings***
The behavior of this crawlspider is based on the given configurations. In this case during scraping a maximum of two requests are made at a time every 10 seconds, a _rotating user agent_[^3] is also implemented.[***click here to view code***](https://github.com/manuelmj/Solar_IAMA/blob/main/ENF_scraper/ENF_scraper/settings.py)

```
31  # See also autothrottle settings and docs
32  DOWNLOAD_DELAY = 10
33  # The download delay setting will honor only one of:
34  CONCURRENT_REQUESTS_PER_DOMAIN = 2
---------------------------------------------------

60  DOWNLOADER_MIDDLEWARES = {
61    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
62    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
63  }
```
also we configure the pipeline for stores the data in a excel file. 
```
72  # Configure item pipelines
73  # See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
74  ITEM_PIPELINES = {
75      'ENF_scraper.pipelines.EnfScraperPipeline': 300,
76   }
77  # name of the file where the scraped data will
78  XLSX_PATH = 'enfsolar_datasheet.xlsx'
```

## **Results**
an excel file with more than 2000 structured data with information about photovoltaic panels containing test data on stc, noct and thermal characteristics[^2]. Also this guide for the implementation of spider crawls using the scrapy framework.


[^1]: [general information of panel](https://es.enfsolar.com/pv/panel-datasheet/crystalline/51157?utm_source=ENF&utm_medium=panel_profile&utm_campaign=enquiry_company_directory&utm_content=4383) 
[^2]:[_excel file_](https://github.com/manuelmj/Solar_IAMA/blob/main/ENF_scraper/ENF_scraper/enfsolar_datasheet.xlsx) 
[^3]: [_rotative user agent_]()
