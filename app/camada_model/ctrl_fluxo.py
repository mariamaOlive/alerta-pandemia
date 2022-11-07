import pandas as pd
from camada_bd.bd_grafo import BDGrafo
from camada_bd.bd_relacional import BDRelacional
from entidades.cidade import Cidade
from entidades.regiao_saude import RegiaoSaude


class CtrlFluxo:

    bdRel = BDRelacional()
    bdGrafo = BDGrafo()
    cacheCidade = None
    cacheRegiaoSaude = None

    def __init__(self):
        pass


    #Funcao retorna dataframe com o fluxo e as info da cidade    
    def percentualFluxo(self, idCidade, tipoFluxo):

        if(self.cacheCidade is None) or (idCidade != self.cacheCidade.id):
            
            # TODO: Fazer consultas paralelamente no banco
            # Busca cidades de destino com conexao no grafo
            fluxo = self.bdGrafo.buscarFluxoCidade(idCidade)
            self.bdGrafo.close()

            # Busca informacoes da cidade de origem
            # Pega as 4 seguintes informacoes -> "cod_ori", "nome_ori", "latitude_ori", "longitude_ori"
            infoCidade = self.bdRel.buscarCidadeCoordenadas(idCidade)
            self.cacheCidade = Cidade(*infoCidade)
            self.cacheCidade.setFluxo(self.construirDfFluxoCidade(fluxo))

        dfFluxoDestino = self.cacheCidade.dfFluxo
        dfFluxo = self.construirDfFluxo(self.cacheCidade.getInfoCidade(), dfFluxoDestino, tipoFluxo)    
        return (self.cacheCidade, dfFluxo)


    #Funcao retorna dataframe com o fluxo da Regiao de Saude e as info da Regiao de Saude
    def percentualFluxoRegiaoSaude(self, idRegiaoSaude, tipoFluxo):

        if(self.cacheRegiaoSaude is None) or (idRegiaoSaude != self.cacheRegiaoSaude.id):
            fluxoSaude = self.bdGrafo.buscarFluxoSaudeRegiao(idRegiaoSaude)
            self.bdGrafo.close() 
            fluxoTransporte = self.bdGrafo.buscarFluxoTransporteRegiao(idRegiaoSaude)
            self.bdGrafo.close() 
            infoRegiaoSaude = self.bdRel.buscarRegiaoCoordenadas(idRegiaoSaude)
            self.cacheRegiaoSaude = RegiaoSaude(*infoRegiaoSaude)
            self.cacheRegiaoSaude.setFluxo(self.construirDfFluxoRegiao(fluxoSaude, fluxoTransporte))

        dfFluxoDestino = self.cacheRegiaoSaude.dfFluxo
        dfFluxo = self.construirDfFluxo(self.cacheRegiaoSaude.getInfoRegiao(), dfFluxoDestino, tipoFluxo)  
        return (self.cacheRegiaoSaude, dfFluxo)

    #Funcao que agrega os dados para serem plotados no mapa
    def construirDfFluxo(self, dadosOrigem, dfFluxo, tipoFluxo):

        dfFluxo["cod_ori"] = dadosOrigem[0]
        dfFluxo["nome_ori"] = dadosOrigem[1]
        dfFluxo["latitude_ori"] = dadosOrigem[2]
        dfFluxo["longitude_ori"] = dadosOrigem[3]

        dfTipoFluxo = pd.DataFrame(dfFluxo[["cod_ori", "nome_ori", "latitude_ori", "longitude_ori",
                        "cod_dest", "nome_dest", "latitude_dest", "longitude_dest", tipoFluxo]])
        
        dfTipoFluxo.rename(columns={tipoFluxo:"fluxo"}, inplace=True)
        dfTipoFluxo.sort_values(by="fluxo", ascending=False, inplace=True)
        dfTipoFluxo = dfTipoFluxo[(dfTipoFluxo["fluxo"]!=0) & (dfTipoFluxo["fluxo"].notna())]          
        return dfTipoFluxo


    #Funcao constroi dfFluxoCidade
    def construirDfFluxoCidade(self, fluxo):
        nomesColunas = ["cod_dest", "nome_dest",  "latitude_dest", "longitude_dest", 
                        "fluxo_geral", "fluxo_aereo", "fluxo_rodo",
                        "saude_alta", "saude_baixa_media"]
        dfFluxo = pd.DataFrame(fluxo, columns=nomesColunas)
        return dfFluxo

    #Funcao constroi dfFluxoRegiao
    def construirDfFluxoRegiao(self, fluxoSaude, fluxoTransporte):
        colunasFluxoSaude = ["cod_dest", "nome_dest", "latitude_dest", "longitude_dest", 
                            "saude_alta", "saude_baixa_media"]
        dfFluxoSaude = pd.DataFrame(fluxoSaude, columns=colunasFluxoSaude)

        colunasFluxoTransporte = ["nome_dest", "cod_dest", "latitude_dest", "longitude_dest", 
                            "fluxo_geral", "fluxo_aereo", "fluxo_rodo"]
        dfFluxoTransporte = pd.DataFrame(fluxoTransporte, columns=colunasFluxoTransporte)

        #Realizar merge dos dois dataframes
        dfFluxo = dfFluxoTransporte.merge(
                    dfFluxoSaude,
                    how='outer', 
                    left_on=["nome_dest", "cod_dest", "latitude_dest", "longitude_dest"], 
                    right_on=["nome_dest", "cod_dest", "latitude_dest", "longitude_dest"]
                    )
        
        return dfFluxo





