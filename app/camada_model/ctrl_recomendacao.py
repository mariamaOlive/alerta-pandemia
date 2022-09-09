import pandas as pd
import camada_bd.bd_grafo as BDGf
import camada_bd.bd_relacional as BDRel


class CtrlRecomendacao:

    bdRel = BDRel.BDRelacional()

    def __init__(self):
        pass

    def calculoRecomendacao(self, idCidade):
        bdGrafo = BDGf.BDGrafo()

        # TODO: Fazer consultas paralelamente no banco
        # Busca cidades de destino com conexao no grafo
        recomendacao = bdGrafo.buscarCidade(idCidade)
        bdGrafo.close()

        # Busca informacoes da cidade de origem
        infoCidade = self.bdRel.buscarCidade(idCidade)

        dfRecomendacao = self.construirDfRecomendacao(infoCidade, recomendacao)
        return dfRecomendacao

    #Funcao que agrega os dados para serem plotados no mapa
    def construirDfRecomendacao(self, dadosCidadeOrigem, listaDadosCidadeDestino):
      
        tupleRecomendacao = [(dadosCidadeOrigem + tuple(cidadeDestino)) for cidadeDestino in listaDadosCidadeDestino]
        nomesColunas = ["cod_ori", "nome_ori", "latitude_ori", "longitude_ori",
                        "cod_dest", "nome_dest", "latitude_dest", "longitude_dest", "score"]
        
        dfRecomendacao = pd.DataFrame(tupleRecomendacao, columns=nomesColunas)
        return dfRecomendacao


