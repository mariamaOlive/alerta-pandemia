import pandas as pd
from camada_bd.bd_grafo import BDGrafo
from camada_bd.bd_relacional import BDRelacional
from entidades.cidade import Cidade


class CtrlSpreader:

    bdRel = BDRelacional()
    bdGrafo = BDGrafo()
    cacheCidade = None

    def __init__(self):
        pass


    def buscarSpreaders(self, idCidadeOrigem):

        queryInfo = self.bdGrafo.buscarMenorCaminho(2611309, "1C")
        self.bdGrafo.close()