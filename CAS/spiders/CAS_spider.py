import scrapy
from scrapy.spiders import CrawlSpider

class CAS_Spider(CrawlSpider):
    name = "CAS_spider"
    start_urls = [
        'https://www.chemicalbook.com/CASDetailList_0_EN.htm'
    ]
    custom_settings = {
        'ITEM_PIPELINES': {'CAS.pipelines.ODBCPipeline': 100,},
        #'ROBOTSTXT_OBEY': False
    }

    def parse_start_url(self, response):
        for row in (response.xpath("//*[@id='ContentPlaceHolder1_ProductClassDetail']/tr")):
            try:
                result = row.xpath("./td/a/text()").getall()
                print(result)
                if result is None:
                    yield {}
                else:
                    yield {
                        'table': "casData",
                        'casNumber': result[0],
                        'casName': result[1]
                    }
                    print ('Yielded: ' + result[0] + " " + result[1])
            except Exception as e:
                print(e)
                print('Error parsing yield.')
        
        for url in (response.xpath("//a[starts-with(@href, '/CASDetailList') and contains(@href, 'EN')]/@href")):
            try:
                yield scrapy.Request('https://www.chemicalbook.com' + url.get(), callback=self.parse_start_url)
            except Exception as e:
                print(e)
                print('Error parsing links')