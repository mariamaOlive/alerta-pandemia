import multiprocessing
from functools import partial
import pandas as pd
import numpy as np


########## Função inicializa matrix de fluxo entre cidades ##########
#retorno: Matriz de Fluxo (numpyArray(nxn)) e dicionario (dict) que mapeia o codigo do municipio com index da matriz
#
#Descrição da Matriz de Fluxo:
#linha: cidade_origem
#coluna: cidade_destino
#valor: qtdViagemDiaria/Populacao --> Probabilidade de uma pessoa da populacao viajar para outra cidade
def criarMatrizFluxo(dfMunicipios, dfFluxo):
    #Inicializar matriz de fluxo
    numMunicipios = dfMunicipios.shape[0]
    matrizFluxo = np.zeros((numMunicipios, numMunicipios))

    #Criando dicionario para indentificar index do municipio na matrixFluxo
    hashIdxMunicipios = {} 
    for idxMunicipio, row in dfMunicipios.iterrows():
        hashIdxMunicipios[row["cod_mun"]] = (idxMunicipio, row["populacao_2021"])
    
    #Adicionando fluxo na matrizFluxo
    for codMunicipio, infoMunicipio in hashIdxMunicipios.items():
        index = infoMunicipio[0]
        populacaoOrigem = infoMunicipio[1]
        
        dfFiltroFluxo = dfFluxo[dfFluxo["cod_origem"]==codMunicipio]
        for idxFluxo, row in dfFiltroFluxo.iterrows():
            idxMunDestino = hashIdxMunicipios[row["cod_destino"]][0]
            matrizFluxo[index][idxMunDestino] = (row["total_pessoas"]/365) / populacaoOrigem

    return matrizFluxo, hashIdxMunicipios


########## Função que calcula a diferenca de Infectado em relacao ao tempo ##########
#retorno: Taxa de variacao de infectados (float)
def taxaVariacao(dia, matrizPopulacao, matrizInfectados, matrizFluxo):

    r = 0.2 #Taxa de contagio
    s = 1 #Ajusta super/subestimativa do fluxo 
    N = matrizPopulacao #Populacao do municipio
    I = matrizInfectados[dia-1] #Numero de Infectado no dia anterior

    #Taxa de variacao infectados interna
    print(np.sum(I))
    dInterno = r*I*((N-I)/N)

    # #Taxa de variacao de infectados devido ao fluxo
    dEntrada =  np.dot(matrizFluxo[:, idxMunicipio].T, matrizInfectados[dia-1]) 
    # dSaida = np.sum(matrizFluxo[idxMunicipio, :]*I)
    # dExterno = dEntrada - dSaida

    # dI = dInterno - s*(dExterno)

    return dInterno



if __name__ == '__main__':

    #Carregando dados de Município
    dfMunicipios = pd.read_csv("../data/integrado/municipio.csv")
    dfMunicipios = dfMunicipios[dfMunicipios['latitude'].notna()]
    dfMunicipios = dfMunicipios.sort_values(by=["cod_mun"])
    dfMunicipios = dfMunicipios.reset_index(drop=True)

    #Carregando dados de fluxo
    dfFluxo = pd.read_csv("../data/calculado/fluxo_prob_qtd.csv")
    dfFluxo = dfFluxo.drop_duplicates()
    dfFluxo = dfFluxo[dfFluxo["cod_origem"].isin(dfMunicipios["cod_mun"])]
    dfFluxo = dfFluxo[dfFluxo["cod_destino"].isin(dfMunicipios["cod_mun"])]

    #Criar matriz de fluxo entre cidades
    matrizFluxo, hashMunicipios = criarMatrizFluxo(dfMunicipios, dfFluxo)

    #Criar matriz de populacao
    matrizPopulacao = dfMunicipios["populacao_2021"].to_numpy()

    #Setar condicoes iniciais
    NUMERO_INFECTADOS = 1
    DIAS = 30

    cidadeInicial = 3550308
    idxCidade = hashMunicipios[cidadeInicial][0]

    #Matriz de Infectados 
    numMunicipios = dfMunicipios.shape[0]
    matrixInfectados =  np.zeros((DIAS, numMunicipios))

    #Adicionar infectados na cidade inicial
    matrixInfectados[0][idxCidade] = NUMERO_INFECTADOS

    #Executar o modelo pelo numero de dias determinados
    # for dia in range(1, DIAS):
    retorno = taxaVariacao(1, matrizPopulacao, matrixInfectados, matrizFluxo)
    print(np.sum(retorno))





    # df_regic = pd.read_csv("../data/integrado/cidades_regic.csv")
    # lista_spreader = df_regic[(df_regic["hierarquia"]=="1A") | (df_regic["hierarquia"]=="1B") | (df_regic["hierarquia"]=="1C") | (df_regic["hierarquia"]=="2A") | (df_regic["hierarquia"]=="2B") | (df_regic["hierarquia"]=="2C")]["cod_mun"].tolist()
    # # lista_spreader = [4209003,3550308, 2611606, 2910800, 2604106,2507507]
    # #Joa, sao paulo, recife, feira de sa, caruaru, joao
    # # lista_spreader = [3550308]
    # #Municipio Incial
    # for municipio_zero in lista_spreader:

    #     #Criando dataframe com resultados
    #     df_si = pd.DataFrame(df_municipios[["cod_mun", "populacao_2021"]])
    #     df_si = df_si.set_index('cod_mun')

    #     #Inicializa todos os municipios com 0 infectados
    #     df_si["dia_0"] = 0.0
    #     df_si.loc[municipio_zero,"dia_0"] = 1 #Somente a cidade zero possui infeccao

    #     #Numero de dias a executar o modelo
    #     nDias =  30
            
    #     #Encontrar as conexoes de todas as cidade
    #     lista_mun = df_municipios["cod_mun"].tolist()
    #     lista_conexoes = []
    #     for cod_mun in lista_mun:
    #         lista_conexoes.append(conexoesCidade(df_fluxo, cod_mun))

    #     #Carrega conexoes possiveis no df
    #     df_si['conexoes'] = lista_conexoes

    #     #Lista de todos os municpios do brasil
    #     lista_mun = df_municipios["cod_mun"].tolist()

    
    #     for dia in range(1, nDias):
    #         infeccoesDia = []
    #         print(dia)
    #         # for cidadeAtual in lista_mun:
    #         pool = multiprocessing.Pool(processes=6)    
    #         infeccoesDia = pool.map(partial(calculoSI, dia=dia, df_si=df_si, df_fluxo=df_fluxo), lista_mun)

    #         sortedInfeccoes = sorted(infeccoesDia, key=lambda tup: tup[0])
    #         listaInfeccoes = [ numInfectados for cod_mun, numInfectados in sortedInfeccoes]


    #         valorCidade = list(filter(lambda x:municipio_zero==x[0], sortedInfeccoes))
    #         # print(sum(listaInfeccoes)-valorCidade[0][1])
    #         df_si[f"dia_{dia}"] = listaInfeccoes

    #     df_si.drop(columns=['conexoes'], inplace=True)
    #     df_si.to_csv(f"../data/calculado/calc_SI_{municipio_zero}.csv", index=True)

