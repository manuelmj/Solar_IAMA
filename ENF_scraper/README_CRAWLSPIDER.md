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

## **Results**


[^1]: [general information of panel](https://es.enfsolar.com/pv/panel-datasheet/crystalline/51157?utm_source=ENF&utm_medium=panel_profile&utm_campaign=enquiry_company_directory&utm_content=4383) 
[^2]:[_excel file_](https://github.com/manuelmj/Solar_IAMA/blob/main/ENF_scraper/ENF_scraper/enfsolar_datasheet.xlsx) 
[^3]: [_rotative user agent_]()
