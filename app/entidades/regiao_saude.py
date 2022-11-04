# Objeto da entidade Cidade 
class RegiaoSaude:

    dfFluxo = None
    listaRedeSentinela = None


    def __init__(self, id, nome, longitude, latitude):
        self.id = id
        self.nome = nome
        self.longitude = longitude
        self.latitude = latitude


    #Retorna as informaçoes principais da cidade
    def getInfoRegiao(self):
        return (self.id, self.nome, self.longitude, self.latitude)


    #Seta uma lista dos fluxos da cidade
    def setFluxo(self, dfFluxo):
        self.dfFluxo = dfFluxo
