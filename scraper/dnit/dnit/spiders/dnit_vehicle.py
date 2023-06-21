import scrapy
import time
from ..json_dnit.read_json import ReadJson
from dnit.items import DnitVehicleItem

def current_milli_time():
    return round(time.time() * 1000)

class DnitVehicleSpider(scrapy.Spider):
    name='DnitVehicle'
    data = []


    def start_requests(self):

        json_file = "/Users/mariama/Documents/dnit/dnit/json_dnit/postos_2017_2.json"
        list_points = ReadJson().get_points(json_file)
        survey = "8"
        
        api_address = "https://servicos.dnit.gov.br/dadospnct/api/pnt/resumo-semanal-veiculos/table?idPesquisa="

        for point in list_points:
            api_request = api_address+survey+"&idPosto="+str(point)+"&lang=brasil&_="+str(current_milli_time())
            yield scrapy.Request(url=api_request, callback=self.parse, meta={'point': point, 'survey': survey})


    def parse(self, response):

        list_vehicle_types = ["Veículo Leve", "Moto", "Ônibus", "Caminhão Leve", "Truck", "Semirreboques", "Semirreboques Especiais", "Reboques"]

        for vehicle, i in zip(list_vehicle_types, range(1, len(list_vehicle_types)+1)):

            dnitVehicleItem = DnitVehicleItem()
            dnitVehicleItem["survey"] = response.meta['survey']
            dnitVehicleItem["point"] = response.meta['point']
            dnitVehicleItem["classe"] = vehicle
            total = response.selector.xpath("//tbody/tr["+str(i)+"]/td[2]/text()").get()
            dnitVehicleItem["total"] = float(total.replace(',','.'))
            percentage = response.selector.xpath("//tbody/tr["+str(i)+"]/td[3]/text()").get()
            dnitVehicleItem["percentage"] = float(percentage.replace(',','.'))

            yield dnitVehicleItem


#Chamadas para cada pesquisa
# scrapy crawl DnitVehicle -o dnit_vehicle_2016_1.csv -t csv
# scrapy crawl DnitVehicle -o dnit_vehicle_2016_2.csv -t csv
# scrapy crawl DnitVehicle -o dnit_vehicle_2017_1.csv -t csv
# scrapy crawl DnitVehicle -o dnit_vehicle_2017_2.csv -t csv