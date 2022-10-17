import multiprocessing
from functools import partial
import pandas as pd



def conexoesCidade(df_fluxo, cidadeAtual):
    df_fluxo_saida = df_fluxo[df_fluxo["cod_origem"] == cidadeAtual]
    df_fluxo_entrada = df_fluxo[df_fluxo["cod_destino"] == cidadeAtual]

    listaCidades_1 = df_fluxo_saida["cod_destino"].tolist()
    listaCidades_2 = df_fluxo_entrada["cod_origem"].tolist()
    listaFinal =  set(listaCidades_1 + listaCidades_2)
    return listaFinal


def calculoDerivada(dia, r, s, I, N, cidadeAtual, df_si, df_fluxo_entrada, df_fluxo_saida ):
    
    dInterna = (r)*I*((N-I)/N)
    listaConexoes = df_si.loc[cidadeAtual,"conexoes"]

    somaEntrada = 0
    somaSaida = 0
    for conexao in listaConexoes:

        #Verifica se há conexao de entrada
        if(conexao in df_fluxo_entrada.index):
            Nd = df_si.loc[conexao,"populacao_2021"] #Populacao da cidade vizinha
            Md = df_fluxo_entrada.loc[conexao, "total_pessoas"]/365 #Numero de pessoas entrando da outra cidade
            Md = Md if Md<(Nd*0.8) else Nd*0.8 #
            Id = df_si.loc[conexao,f"dia_{dia-1}"] # Numero de infectados da cidade vizinha
            resultadoEntrada = (Md/Nd)*Id
            somaEntrada += resultadoEntrada
            # if(conexao==3550308):
            #     print("conexoes: ",len(listaConexoes))
            #     print("Id", Id)
            #     print("Md", Md)             
            #     print("Nd", Nd)

        #Verifica se há conexao de saída
        if(conexao in df_fluxo_saida.index):
            M = df_fluxo_saida.loc[conexao, "total_pessoas"]/365
            M = M if M<(N*0.8) else N*0.8
            resultadoSaida = (M/N)*I
            somaSaida += resultadoSaida
            # if(conexao==3550308):
            #     print("I", I)
            #     print("M", M)


    dExterna = s*(somaEntrada - somaSaida)
    # dExternaCorrigida = dExterna if dExterna>0 else 0
    # if(cidadeAtual==3304557):
    #     print("dExterna", dExternaCorrigida)
    # print((I, dExternaCorrigida, dInterna))
    dTotal = dInterna + dExterna
    return dTotal if dTotal>0 else 0

def calculoSI(cidadeAtual, dia, df_si, df_fluxo):
    
    r = 0.2
    s = 1
    N = df_si.loc[cidadeAtual,"populacao_2021"]#populacao do conjunto
    I = df_si.loc[cidadeAtual,f"dia_{dia-1}"] # Infectados na populacao

    #Valor da contaminacao interna
    # dInterna = (1+r)*I*((N-I)/N)

    #Calculo do Valor da contaminacao externa
    #Fitrar todas as ligacoes que a cidade possui (Entrada e Saída de pessoas)
    df_fluxo_saida = pd.DataFrame(df_fluxo[df_fluxo["cod_origem"] == cidadeAtual]).set_index('cod_destino')
    df_fluxo_entrada = pd.DataFrame(df_fluxo[df_fluxo["cod_destino"] == cidadeAtual]).set_index('cod_origem')


    



    # dt = 1
    # dt2 = dt/2.0
    # k1 = calculoDerivada(dia, r, s, I, N, cidadeAtual, df_si, df_fluxo_entrada, df_fluxo_saida )
    # k2 = calculoDerivada(dia, r, s, I + dt2*k1, N, cidadeAtual, df_si, df_fluxo_entrada, df_fluxo_saida )
    # k3 = calculoDerivada(dia, r, s, I + dt2*k2, N, cidadeAtual, df_si, df_fluxo_entrada, df_fluxo_saida )
    # k4 = calculoDerivada(dia, r, s, I + dt2*k3, N, cidadeAtual, df_si, df_fluxo_entrada, df_fluxo_saida )
    # novoI = I + (dt/6.0)*(k1 + 2*k2 + 2*k3 + k4)

    novoI = calculoDerivada(dia, r, s, I, N, cidadeAtual, df_si, df_fluxo_entrada, df_fluxo_saida )
    # df_si.loc[cidadeAtual,f"dia_{dia}"] = novoI
    # print(novoI)
    # infeccoesDia.append(novoI)
    # if(cidadeAtual==2803302):
    #     print("NovoI: ", novoI)
    #     print("dInterna: ", dInterna)
    #     print("dExterna: ", dExternaCorrigida)
    #     print("I: ", I)

    return (cidadeAtual,novoI)

if __name__ == '__main__':

    #Carregando dados de Município
    df_municipios = pd.read_csv("../data/integrado/municipio.csv")
    df_municipios= df_municipios[df_municipios['latitude'].notna()]
    df_municipios= df_municipios.sort_values(by=["cod_mun"])

    #Carregando dados de fluxo
    df_fluxo = pd.read_csv("../data/calculado/fluxo_prob_qtd.csv")
    df_fluxo = df_fluxo.drop_duplicates()
    df_fluxo= df_fluxo[df_fluxo["cod_origem"].isin(df_municipios["cod_mun"])]
    df_fluxo= df_fluxo[df_fluxo["cod_destino"].isin(df_municipios["cod_mun"])]


    df_regic = pd.read_csv("../data/integrado/cidades_regic.csv")
    lista_spreader = df_regic[(df_regic["hierarquia"]=="1A") | (df_regic["hierarquia"]=="1B") | (df_regic["hierarquia"]=="1C") | (df_regic["hierarquia"]=="2A") | (df_regic["hierarquia"]=="2B") | (df_regic["hierarquia"]=="2C")]["cod_mun"].tolist()
    # lista_spreader = [4209003,3550308, 2611606, 2910800, 2604106,2507507]
    #Joa, sao paulo, recife, feira de sa, caruaru, joao
    # lista_spreader = [3550308]
    #Municipio Incial
    for municipio_zero in lista_spreader:

        #Criando dataframe com resultados
        df_si = pd.DataFrame(df_municipios[["cod_mun", "populacao_2021"]])
        df_si = df_si.set_index('cod_mun')

        #Inicializa todos os municipios com 0 infectados
        df_si["dia_0"] = 0.0
        df_si.loc[municipio_zero,"dia_0"] = 1 #Somente a cidade zero possui infeccao

        #Numero de dias a executar o modelo
        nDias =  30
            
        #Encontrar as conexoes de todas as cidade
        lista_mun = df_municipios["cod_mun"].tolist()
        lista_conexoes = []
        for cod_mun in lista_mun:
            lista_conexoes.append(conexoesCidade(df_fluxo, cod_mun))

        #Carrega conexoes possiveis no df
        df_si['conexoes'] = lista_conexoes

        #Lista de todos os municpios do brasil
        lista_mun = df_municipios["cod_mun"].tolist()

    
        for dia in range(1, nDias):
            infeccoesDia = []
            print(dia)
            # for cidadeAtual in lista_mun:
            pool = multiprocessing.Pool(processes=6)    
            infeccoesDia = pool.map(partial(calculoSI, dia=dia, df_si=df_si, df_fluxo=df_fluxo), lista_mun)

            sortedInfeccoes = sorted(infeccoesDia, key=lambda tup: tup[0])
            listaInfeccoes = [ numInfectados for cod_mun, numInfectados in sortedInfeccoes]


            valorCidade = list(filter(lambda x:municipio_zero==x[0], sortedInfeccoes))
            # print(sum(listaInfeccoes)-valorCidade[0][1])
            df_si[f"dia_{dia}"] = listaInfeccoes

        df_si.drop(columns=['conexoes'], inplace=True)
        df_si.to_csv(f"../data/calculado/calc_SI_{municipio_zero}.csv", index=True)

