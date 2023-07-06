import pandas as pd
from camada_bd.bd_relacional import BDRelacional
from entidades.cidade import Cidade

class CtrlAtributosCidade:
    bdRel = BDRelacional()
    nomeColunasMunicipio = ["cod_mun", "nome_mun","latitude","longitude", "populacao_2021",
                            "densidade_2021","area", "uf","nome_uf","cod_uf","pais","pib","hierarquia",
                            "nome_hierarquia","indice_atracao","ia_saude_bm","ia_saude_a","ia_aeroporto",
                            "ia_transporte","num_leitos", "total_pais", "total_cidade", "total_outras_cidades",
                            "regiao_saude", "rede_sentinela"]


    def __init__(self):
        pass
    def carregarTodasCidades(self):
        
        # Busca informacoes da cidade 
        cidades = self.bdRel.buscarTodasCidadesComSentinela()

        #Transforma em um df
        dfCidades = pd.DataFrame(cidades, columns=self.nomeColunasMunicipio)

        #Trata coluna de rede sentinela, transforma na classe list
        dfCidades['rede_sentinela'] = dfCidades['rede_sentinela'].str.split(',')

        return dfCidades

    
    def carregarListaCidades(self, lista):
        
        # Busca informacoes da cidade 
        cidades = self.bdRel.buscarTodasCidadesComSentinela()

        #Transforma em um df
        dfCidades = pd.DataFrame(cidades, columns=self.nomeColunasMunicipio)

        #Trata coluna de rede sentinela, transforma na classe list
        dfCidades['rede_sentinela'] = dfCidades['rede_sentinela'].str.split(',')
        dfCidadesFiltrado = dfCidades[dfCidades['cod_mun'].isin(lista)]

        return dfCidadesFiltrado


    #Busca toda as informações relativas a uma cidade
    def carregarCidade(self, idCidade)->Cidade:
        # Busca informacao de uma cidade 
        pass