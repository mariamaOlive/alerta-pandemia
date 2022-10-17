import pandas as pd
from camada_bd.bd_grafo import BDGrafo
from camada_bd.bd_relacional import BDRelacional
from entidades.path import Path



class CtrlSpreader:

    bdRel = BDRelacional()
    bdGrafo = BDGrafo()
    cacheCidade = None

    def __init__(self):
        pass


    def buscarSpreaders(self, idCidadeOrigem):

        strIdCidadeOrigem = str(idCidadeOrigem)
        queryInfo = self.bdGrafo.buscarMenorCaminho(strIdCidadeOrigem, "1C")
        self.bdGrafo.close()

        paths = self.tratarCaminho(queryInfo)

        for caminho in paths:
            print(caminho.probabilidade)

    def tratarCaminho(self, query):

        listaCaminhos = []
        for probInvertida, caminho in query:
            probabilidade = self.calcularProbabilidade(probInvertida)
            listaCaminhos.append(Path(caminho, probabilidade))

        return listaCaminhos
         

    def calcularProbabilidade(self, listaProbabilidades):

        probCorrigida = 1
        listaProbabilidades.reverse()
        for idx, prob in enumerate(listaProbabilidades[:-1]):
            probCorrigida *= (1 - (prob-listaProbabilidades[idx+1]))
        
        return probCorrigida
