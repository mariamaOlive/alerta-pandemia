import pandas as pd
import camada_bd.bd_grafo as BDGf
import camada_bd.bd_relacional as BDRel


class CtrlRecomendacao:

    bdRel = BDRel.BDRelacional()

    def __init__(self):
        pass

    def calculoRecomendacao(self, idCidade, tipoFluxo):
        bdGrafo = BDGf.BDGrafo()
        # TODO: Fazer consultas paralelamente no banco
        # Busca cidades de destino com conexao no grafo
        recomendacao = bdGrafo.buscarCidade(idCidade)
        bdGrafo.close()

        # Busca informacoes da cidade de origem
        infoCidade = self.bdRel.buscarCidade(idCidade)

        dfRecomendacao = self.construirDfRecomendacao(infoCidade, recomendacao, tipoFluxo)
        return dfRecomendacao[:20]

    #Funcao que agrega os dados para serem plotados no mapa
    def construirDfRecomendacao(self, dadosCidadeOrigem, listaDadosCidadeDestino, tipoFluxo):

        tupleRecomendacao = [(dadosCidadeOrigem + tuple(cidadeDestino)) for cidadeDestino in listaDadosCidadeDestino]
        nomesColunas = ["cod_ori", "nome_ori", "latitude_ori", "longitude_ori",
                        "nome_dest", "cod_dest", "latitude_dest", "longitude_dest", 
                        "fluxo_geral", "fluxo_aereo", "fluxo_rodo"]

        dfRecomendacao = pd.DataFrame(tupleRecomendacao, columns=nomesColunas)
        dfTipoFluxo = pd.DataFrame(dfRecomendacao[["cod_ori", "nome_ori", "latitude_ori", "longitude_ori",
                        "nome_dest", "cod_dest", "latitude_dest", "longitude_dest", tipoFluxo]])
        
        dfTipoFluxo.rename(columns={tipoFluxo:"fluxo"}, inplace=True)
        dfTipoFluxo.sort_values(by="fluxo", ascending=False, inplace=True)
        dfTipoFluxo = dfTipoFluxo[dfTipoFluxo["fluxo"]!=0]          
        return dfTipoFluxo


