import multiprocessing
from functools import partial
import pandas as pd
import numpy as np



########## Método de cálculo de ODE - Runge-Kutta ##########
#retorno: Variacao calulada
def calcularODE(funcao, *args):

    dt = 1
    dt2 = dt/2.0
    k1 = funcao(args[0], args[1], args[2])
    k2 = funcao(args[0], args[1] + dt2*k1, args[2])
    k3 = funcao(args[0], args[1] + dt2*k2, args[2])
    k4 = funcao(args[0], args[1] + dt2*k3, args[2])
    novoI = args[1] + (dt/6.0)*(k1 + 2*k2 + 2*k3 + k4)
    return novoI

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
            matrizFluxo[index][idxMunDestino] = (row["passageiros_total"]/365) / populacaoOrigem

    return matrizFluxo, hashIdxMunicipios


########## Função que calcula a diferenca de Infectado em relacao ao tempo ##########
#retorno: Taxa de variacao de infectados em todas cidades (npArray de float)
def calcularTaxaVariacao(matrizPopulacao, infectadosDiaAnterior, matrizFluxo):

    r = 0.2 #Taxa de contagio
    s = 1 #Ajusta super/subestimativa do fluxo 
    N = matrizPopulacao #Populacao do municipio
    I = infectadosDiaAnterior #Numero de Infectado no dia anterior
    M = matrizFluxo

    #Taxa de variacao infectados interna
    dInterno = r*I*((N-I)/N)

    #Taxa de variacao de infectados devido ao fluxo
    # print("Infectados ",I[3829])
    # print("Probabilidade ", M[3829].sum())
    dSaida = M.sum(axis=1)*I #Pessoas infectadas que saem da cidade
    # print("Saida ",dSaida[3829])
    dEntrada = np.matmul(I, M) #Pessoas infectadas que entram na cidade
    # print("Entrada ",dEntrada[3829])
    dExterno = dEntrada - dSaida

    #Taxa de variacao total
    dI = dInterno + s*(dExterno)
    return dI.clip(min=0) #Torna positivo



if __name__ == '__main__':

    #Carregando dados de Município
    dfMunicipios = pd.read_csv("../data/integrado/municipio.csv")
    dfMunicipios = dfMunicipios[dfMunicipios['latitude'].notna()]
    dfMunicipios = dfMunicipios.sort_values(by=["cod_mun"])
    dfMunicipios = dfMunicipios.reset_index(drop=True)

    #Carregando dados de fluxo
    dfFluxo = pd.read_csv("../data/calculado/calculo_qtd_fluxo.csv")
    dfFluxo = dfFluxo.drop_duplicates()
    dfFluxo = dfFluxo[dfFluxo["cod_origem"].isin(dfMunicipios["cod_mun"])]
    dfFluxo = dfFluxo[dfFluxo["cod_destino"].isin(dfMunicipios["cod_mun"])]

    #Criar matriz de fluxo entre cidades
    matrizFluxo, hashMunicipios = criarMatrizFluxo(dfMunicipios, dfFluxo)

    #Criar matriz de populacao
    matrizPopulacao = dfMunicipios["populacao_2021"].to_numpy()

    #Setar condicoes iniciais
    NUMERO_INFECTADOS = 1
    DIAS = 60

    ##TODO:Teste remover
    saida = np.count_nonzero(matrizFluxo, axis=0)
    entrada = np.count_nonzero(matrizFluxo, axis=1)

    #TODO: Remover print
    # print("Sai: ", saida[hashMunicipios[3550308][0]])
    # print("Entra: ", entrada[hashMunicipios[3550308][0]])
    # print(hashMunicipios[3550308][0])


    listaAnalise = []
    df_regic = pd.read_csv("../data/integrado/cidades_regic.csv")
    listaSpreader = df_regic[(df_regic["hierarquia"]=="1A") | (df_regic["hierarquia"]=="1B") | (df_regic["hierarquia"]=="1C") | (df_regic["hierarquia"]=="2A") | (df_regic["hierarquia"]=="2B") | (df_regic["hierarquia"]=="2C")]["cod_mun"].tolist()
    # listaSpreader = df_regic[(df_regic["hierarquia"]=="1A") | (df_regic["hierarquia"]=="1B") | (df_regic["hierarquia"]=="1C") ]["cod_mun"].tolist()
    # listaSpreader = df_regic["cod_mun"].tolist()
    for cidadeInicial in listaSpreader: 
        # cidadeInicial = 3550308
        print("Municipio: ", cidadeInicial)
        idxCidade = hashMunicipios[cidadeInicial][0]

        #Matriz de Infectados 
        numMunicipios = dfMunicipios.shape[0]
        matrixInfectados =  np.zeros((DIAS, numMunicipios))

        #Adicionar infectados na cidade inicial
        matrixInfectados[0][idxCidade] = NUMERO_INFECTADOS

        #Executar o modelo pelo numero de dias determinados
        for dia in range(1, DIAS):
            matrixInfectados[dia] = matrixInfectados[dia -1] + calcularTaxaVariacao(matrizPopulacao, matrixInfectados[dia-1], matrizFluxo)
            # matrixInfectados[dia] = calcularODE(calcularTaxaVariacao, matrizPopulacao, matrixInfectados[dia-1], matrizFluxo)


        #Criar dataframe com os dados de infectados
        dfSI = pd.DataFrame(matrixInfectados.T, columns=["dia_" + str(dia) for dia in range(DIAS)])
        dfSI = pd.concat([dfMunicipios[["cod_mun","nome_mun"]], dfSI], axis=1, join='inner')
        # dfSI.to_csv(f"../data/calculado/calc_SI_{cidadeInicial}.csv", index=False)

        filtro_cidade = dfSI["cod_mun"]==cidadeInicial
        num_cidade = dfSI[filtro_cidade][f"dia_{DIAS-1}"].sum()
        num_espalhamento = dfSI[~filtro_cidade][f"dia_{DIAS-1}"].sum()
        num_total = num_cidade + num_espalhamento
        listaAnalise.append((cidadeInicial, num_cidade, num_espalhamento, num_total))


    df_analise = pd.DataFrame(listaAnalise, columns=["cod_mun","cidade", "espalhamento", "total"])
    df_analise.to_csv(f"../data/calculado/spreaders.csv", index=False)

