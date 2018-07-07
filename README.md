# Web Scraping

Web scraping, web harvesting, or web data extraction is data scraping used for extracting data from websites.Web scraping software may access the World Wide Web directly using the Hypertext Transfer Protocol, or through a web browser. While web scraping can be done manually by a software user, the term typically refers to automated processes implemented using a bot or web crawler. It is a form of copying, in which specific data is gathered and copied from the web, typically into a central local database or spreadsheet, for later retrieval or analysis.

### Scrapy ([Tutorials](https://docs.scrapy.org/en/latest/intro/tutorial.html))

1. scrapy startproject <project-name>
2. scrapy crawl <spider-name> (E.g. : Do not see the file name `quotes_spider.py`, see `name = "quotes"` inside sipder's class , `scrapy crawl quotes`)
3. scrapy shell "url"
4. response.css('title')
5. response.css('title::text').extract()
6. response.css('title::text').extract_first()
7. response.css('title::text')[0].extract()
8. scrapy crawl quotes -o quotes.json
9. response.css('li.next a::attr(href)').extract_first()