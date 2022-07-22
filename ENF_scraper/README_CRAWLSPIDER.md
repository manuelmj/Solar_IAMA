# CrawlSpider

## ***Table of contenst***
- [X] 1. [**Spider**](https://github.com/manuelmj/Solar_IAMA/tree/main/ENF_scraper/ENF_scraper/spiders)
- [X] 2. [**Items**](https://github.com/manuelmj/Solar_IAMA/blob/main/ENF_scraper/ENF_scraper/items.py)
- [X] 3. [**Pipelines**](https://github.com/manuelmj/Solar_IAMA/blob/main/ENF_scraper/ENF_scraper/pipelines.py)
- [X] 1. [**Settings**](https://github.com/manuelmj/Solar_IAMA/blob/main/ENF_scraper/ENF_scraper/settings.py)

## ***Abstrac***
This is a crawlSpider in charge of scraping [_ENFsolar_](https://es.enfsolar.com), this bot downloads information of photovoltaic panels, and reorganizes the data in data structures, for this we use more than 20 links of manufacturer's pages that contain information of their panels as data in _STC_, _NOCT_ and _THERMAL CHARACTERISTICS_ conditions, these three categories contain relevant information for this research.

## ***Spiders***


## ***Items***
The elements necessary for the structuring of the data are found in this section, divided into four categories containing data on STC and NOCT conditions, thermal characteristics and basic information on the photovoltaic panel. [***click here to view code***](https://github.com/manuelmj/Solar_IAMA/blob/main/ENF_scraper/ENF_scraper/items.py)

## ***Pipleines***
This pipeline stores the data in an excel file structured as follows[^1] : 

|company name |pv name|pv model|pv_type|pmax stc|vmax stc|voc stc|isc stc|imax stc|efficiency stc|tolerance|pmax noct|vmax noct|voc noct|isc noct|imax noct|temp noct|temp range|temp pmax coef|temp voc coef|temp isc coef|
| :---|:---:|:---:| :---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---:|

[***click here to view code***](https://github.com/manuelmj/Solar_IAMA/blob/main/ENF_scraper/ENF_scraper/pipelines.py)

## ***Settings***
The behavior of this crawlspider is based on the given configurations. In this case during scraping a maximum of two requests are made at a time every 10 seconds, a _rotating user agent_[^2] is also implemented. [***click here to view code***](https://github.com/manuelmj/Solar_IAMA/blob/main/ENF_scraper/ENF_scraper/settings.py)

## **Results**


[^1]: [_excel file_](https://github.com/manuelmj/Solar_IAMA/blob/main/ENF_scraper/ENF_scraper/enfsolar_datasheet.xlsx) 
[^2]: [_rotative user agent_]()
