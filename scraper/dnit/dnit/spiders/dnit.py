import scrapy
import time
from ..json_dnit.read_json import ReadJson
from dnit.items import DnitItem

def current_milli_time():
    return round(time.time() * 1000)

class DnitSpider(scrapy.Spider):
    name='Dnit'
    data = []


    def start_requests(self):

        json_file = "dnit/json_dnit/postos_2017_2.json"
        list_points = ReadJson().get_points(json_file)
        survey = "8"
        
        api_address = "https://servicos.dnit.gov.br/dadospnct/api/pnt/resumo-semanal-dia/table?idPesquisa="

        for point in list_points:
            api_request = api_address+survey+"&idPosto="+str(point)+"&lang=brasil&_="+str(current_milli_time())
            yield scrapy.Request(url=api_request, callback=self.parse, meta={'point': point, 'survey': survey})


    def parse(self, response):

        for day in range(1,8):
            dnitItem = DnitItem()
            dnitItem["survey"] = response.meta['survey']
            dnitItem["point"] = response.meta['point']
            dnitItem["day"] = day
            dnitItem["date"] = response.selector.xpath("//tbody/tr["+str(day)+"]/td[1]/text()").get()[:5]
            dnitItem["crescente"] = response.selector.xpath("//tbody/tr["+str(day)+"]/td[2]/text()").get()
            dnitItem["decrescente"] = response.selector.xpath("//tbody/tr["+str(day)+"]/td[3]/text()").get()
            dnitItem["total"] = response.selector.xpath("//tbody/tr["+str(day)+"]/td[4]/text()").get()

            yield dnitItem
            # print(response.selector.xpath("//tbody/tr[1]/td[1]/text()").get())
            
#Chamadas para cada pesquisa
# scrapy crawl Dnit -o dnit2016_1.csv -t csv
# scrapy crawl Dnit -o dnit2016_2.csv -t csv
# scrapy crawl Dnit -o dnit2017_1.csv -t csv
# scrapy crawl Dnit -o dnit2017_2.csv -t csv