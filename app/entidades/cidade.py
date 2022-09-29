# Objeto da entidade Cidade 
class Cidade:

    fluxo = None
    dfFluxo = None

    def __init__(self, id, nome, longitude, latitude):
        self.id = id
        self.nome = nome
        self.longitude = longitude
        self.latitude = latitude

    
    def getInfoCidade(self):
        return (self.id, self.nome, self.longitude, self.latitude)

    def setFluxo(self, fluxo):
        self.fluxo = fluxo

    