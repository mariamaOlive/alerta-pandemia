import pandas as pd
import camada_bd.bd_relacional as BDRel


class CtrlAtributosCidade:

    bdRel = BDRel.BDRelacional()
    nomeColunasMunicipio = ["cod_mun","cod_uf","cod_reg_saude","nome_mun","latitude","longitude",
                        "populacao_2011","populacao_2021","densidade_2021","area","uf","nome_uf",
                        "pais","pib","hierarquia","nome_hierarquia","indice_atracao","ia_saude_bm",
                        "ia_saude_a","ia_aeroporto","ia_transporte","num_leitos"]

    def __init__(self):
        pass

    def carregarTodasCidades(self):
        
        # Busca informacoes da cidade de origem
        cidades = self.bdRel.buscarTodasCidades()
        dfCidades = pd.DataFrame(cidades, columns=self.nomeColunasMunicipio)
        return dfCidades

    
    def carregarCidade(self, idCidade):

        # Busca informacao de uma cidade 
        pass

