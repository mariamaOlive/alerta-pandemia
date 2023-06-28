import scrapy
import time
from ..json_dnit.read_json import ReadJson
from dnit.items import DnitHourItem

def current_milli_time():
    return round(time.time() * 1000)

class DnitHourSpider(scrapy.Spider):
    name='DnitHour'
    data = []


    def start_requests(self):

        json_file = "dnit/json_dnit/postos_2017_2.json"
        list_points = ReadJson().get_points(json_file)
        survey = "8"
        starting_day = 18
 
        api_address = "https://servicos.dnit.gov.br/dadospnct/api/pnt/resumo-horario?idPesquisa="

        for point in list_points:
            for day in range(starting_day, starting_day+8):
                api_request = api_address+survey+"&idPosto="+str(point)+"&dia="+str(day)+"&_="+str(current_milli_time())
                yield scrapy.Request(url=api_request, callback=self.parse, meta={'point': point, 'survey': survey, 'day': day})


    def parse(self, response):

        #Getting json response
        json_response = response.json()
        list_data = json_response["dado"]["dado"]
       
        for data in list_data:
            #Creating item to be saved
            dnitHourItem = DnitHourItem()
            dnitHourItem["survey"] = response.meta['survey']
            dnitHourItem["point"] = response.meta['point']
            dnitHourItem["day"] = response.meta['day']

            for key in data:
                dnitHourItem[key] = data[key] 

            yield dnitHourItem



#Chamadas para cada pesquisa
# scrapy crawl DnitHour -o dnit_hour_2016_1.csv -t csv
# scrapy crawl DnitHour -o dnit_hour_2016_2.csv -t csv
# scrapy crawl DnitHour -o dnit_hour_2017_1.csv -t csv
# scrapy crawl DnitHour -o dnit_hour_2017_2.csv -t csv

