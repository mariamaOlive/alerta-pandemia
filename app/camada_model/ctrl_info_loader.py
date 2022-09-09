import pandas as pd
import camada_bd.bd_relacional as BDRel


class CtrlInfoLoader:

    dfEstados = None
    bdRel = BDRel.BDRelacional()

    def __init__(self):
        self.dfEstados = self.carregarEstados()


    #Retorna todos estados brasileiros em ordem asc
    def carregarEstados(self):
        listaEstados = self.bdRel.buscarEstados()
        dfEstados = pd.DataFrame(listaEstados, columns=['cod_uf', 'uf', 'nome_uf'])
        return dfEstados


    #Retorna todos as cidades de um estados em ordem asc
    def carregarCidadesPorEstado(self, estadoId):
        listaCidades = self.bdRel.buscarCidadesPorEstado(estadoId)
        dfCidades = pd.DataFrame(listaCidades, columns=['cod_mun', 'nome_mun'])
        return dfCidades
