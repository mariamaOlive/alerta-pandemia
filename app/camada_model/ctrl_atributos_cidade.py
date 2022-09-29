import pandas as pd
from camada_bd.bd_relacional import BDRelacional
from entidades.cidade import Cidade


class CtrlAtributosCidade:

    bdRel = BDRelacional()
    nomeColunasMunicipio = ["cod_mun","cod_uf","cod_reg_saude","nome_mun","latitude","longitude",
                        "populacao_2011","populacao_2021","densidade_2021","area","uf","nome_uf",
                        "pais","pib","hierarquia","nome_hierarquia","indice_atracao","ia_saude_bm",
                        "ia_saude_a","ia_aeroporto","ia_transporte","num_leitos","rede_sentinela"]

    def __init__(self):
        pass

    def carregarTodasCidades(self):
        
        # Busca informacoes da cidade 
        cidades = self.bdRel.buscarTodasCidadesComSentinela()
        
        dfCidades = pd.DataFrame(cidades, columns=self.nomeColunasMunicipio)
        return dfCidades


    #Busca toda as informações relativas a uma cidade
    def carregarCidade(self, idCidade)->Cidade:

        # Busca informacao de uma cidade 
        pass



