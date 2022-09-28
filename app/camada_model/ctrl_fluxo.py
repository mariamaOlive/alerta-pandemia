from linecache import cache
import pandas as pd
import camada_bd.bd_grafo as BDGf
import camada_bd.bd_relacional as BDRel
from entidades.cidade import Cidade


class CtrlFluxo:

    bdRel = BDRel.BDRelacional()
    cacheCidade = None

    def __init__(self):
        pass


    #Funcao retorna dataframe com o fluxo e as info da cidade    
    def percentualFluxo(self, idCidade, tipoFluxo, qtdCidades=20):

        if(self.cacheCidade is None) or (idCidade != self.cacheCidade.id):
            bdGrafo = BDGf.BDGrafo()
            # TODO: Fazer consultas paralelamente no banco
            # Busca cidades de destino com conexao no grafo
            fluxo = bdGrafo.buscarFluxoCidade(idCidade)
            bdGrafo.close()

            # Busca informacoes da cidade de origem
            # Pega as 4 seguintes informacoes -> "cod_ori", "nome_ori", "latitude_ori", "longitude_ori"
            infoCidade = self.bdRel.buscarCidadeCoordenadas(idCidade)
            self.cacheCidade = Cidade(*infoCidade)
            self.cacheCidade.setFluxo(fluxo)

        dfFluxo = self.construirDfFluxo(self.cacheCidade.getInfoCidade(), self.cacheCidade.fluxo, tipoFluxo)    
        return (self.cacheCidade, dfFluxo[:qtdCidades])


    #Funcao que agrega os dados para serem plotados no mapa
    def construirDfFluxo(self, dadosCidadeOrigem, listaDadosCidadeDestino, tipoFluxo):

        tupleFluxo = [(dadosCidadeOrigem + tuple(cidadeDestino)) for cidadeDestino in listaDadosCidadeDestino]
        nomesColunas = ["cod_ori", "nome_ori", "latitude_ori", "longitude_ori",
                        "nome_dest", "cod_dest", "latitude_dest", "longitude_dest", 
                        "fluxo_geral", "fluxo_aereo", "fluxo_rodo",
                        "saude_alta", "saude_baixa_media"]

        dfFluxo = pd.DataFrame(tupleFluxo, columns=nomesColunas)
        dfTipoFluxo = pd.DataFrame(dfFluxo[["cod_ori", "nome_ori", "latitude_ori", "longitude_ori",
                        "cod_dest", "nome_dest", "latitude_dest", "longitude_dest", tipoFluxo]])
        
        dfTipoFluxo.rename(columns={tipoFluxo:"fluxo"}, inplace=True)
        dfTipoFluxo.sort_values(by="fluxo", ascending=False, inplace=True)
        dfTipoFluxo = dfTipoFluxo[(dfTipoFluxo["fluxo"]!=0) & (dfTipoFluxo["fluxo"].notna())]          
        return dfTipoFluxo





