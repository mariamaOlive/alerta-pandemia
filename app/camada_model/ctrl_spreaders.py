import pandas as pd
from camada_bd.bd_grafo import BDGrafo
from camada_bd.bd_relacional import BDRelacional
from entidades.path import Path
from entidades.cidade import Cidade


class CtrlSpreader:

    bdRel = BDRelacional()
    bdGrafo = BDGrafo()
    cacheCidade = None

    def __init__(self):
        pass

    
    #Realiza a query no BD e retorna caminhos
    def buscarSpreaders(self, idCidadeOrigem):

        strIdCidadeOrigem = str(idCidadeOrigem)
        queryInfo = self.bdGrafo.buscarMenorCaminho(strIdCidadeOrigem, "1C")
        self.bdGrafo.close()

        paths = self.tratarCaminho(queryInfo)
        return paths


    def buscarTodasPropagacoes(self):
        queryInfo = self.bdRel.buscarTotalPropacao()
        dfPropagacao = pd.DataFrame(queryInfo, columns=['cod_mun', 'total_pais', 'total_cidade', 'total_outras_cidades'])
        return dfPropagacao


    #Cria a lista de possíveis caminho de acordo com a resposta da query
    def tratarCaminho(self, query):
        listaCaminhos = []
        for probTotal, custoPath, caminho in query:
            probabilidade = abs(probTotal)
            caminhoTratado = self.gerarCaminho(caminho)
            listaCaminhos.append(Path(caminhoTratado, probabilidade))

        return listaCaminhos
         

    #Funcao gera o caminho com o objeto cidade
    def gerarCaminho(self, path):
        listaCidades = []

        for cidade in path:
            listaCidades.append(Cidade(cidade.get("cod_mun"), cidade.get("nome"),  cidade.get("longitude"), cidade.get("latitude")))

        return listaCidades