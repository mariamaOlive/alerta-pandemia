import pandas as pd
import camada_bd.bd_relacional as BDRel



class InfoLoader:

    dfEstados = None
    bdRel = BDRel.BDRelacional()

    def __init__(self):
        self.dfEstados = self.carregarEstados()

    #Retorna todos estados brasileiros em ordem asc
    def carregarEstados(self):
        listaEstados = self.bdRel.carregarEstados()
        print(self.bdRel.carregarEstados())
        dfEstados = pd.DataFrame(listaEstados, columns=['cod_uf', 'uf', 'nome_uf'])

        return dfEstados


    #Retorna todos as cidades de um estados em ordem asc
    def carregarCidadesPorEstado(self, estadoId):
        pass
