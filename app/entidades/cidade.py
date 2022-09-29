# Objeto da entidade Cidade 
class Cidade:

    fluxo = None
    dfFluxo = None
    listaRedeSentinela = None


    def __init__(self, id, nome, longitude, latitude):
        self.id = id
        self.nome = nome
        self.longitude = longitude
        self.latitude = latitude


    #Retorna as informaçoes principais da cidade
    def getInfoCidade(self):
        return (self.id, self.nome, self.longitude, self.latitude)


    #Seta uma lista dos fluxos da cidade
    def setFluxo(self, fluxo):
        self.fluxo = fluxo

    
    #Seta a lista da rede sentinela da cidade
    # def setRedeSentinela(self, listaRedeSentinela):
    #     self.listaRedeSentinela = listaRedeSentinela
    