import plotly.express as px

def carregaBarChart(df):

    dfBarChart = df
    valor = round(dfBarChart['fluxo'],3)
    
    fig = px.bar(dfBarChart, 
     x= valor, y="nome_dest", orientation='h', text_auto=True,
     color_discrete_sequence=px.colors.qualitative.Pastel[1:], template="plotly_dark",
     labels={'fluxo':'Fluxos', 'nome_dest':'Destino'},
        ).update_layout(margin={"r":0,"t":46,"l":0,"b":6}).update_xaxes(visible=True).update_xaxes(title_text='Probabilidade').update_traces(texttemplate='%{x:.d}')

    fig.update_layout(title_text='Os Maiores Fluxos', 
                    title_x=0.5,
                    yaxis = {
                        'tickmode': 'array',
                        'tickvals': list(range(dfBarChart.shape[0])),
                        'ticktext': dfBarChart['nome_dest'].apply(formatarNomeCidade).tolist(),
                        }
                    )

    fig.update_traces(marker_color='rgb(255, 151, 29)', marker_line_color='rgb(255, 255, 255)',
                  marker_line_width=1.5)

    fig.update_layout(yaxis=dict(autorange="reversed"))
    
    return fig

#Funçao que formata os nomes das Cidades
def formatarNomeCidade(nome):
        
    nomeFormatado = nome
    if("Arranjo Populacional Internacional" in nomeFormatado):
        nomeFormatado = nomeFormatado.replace("Arranjo Populacional Internacional", "API" )    
    elif("Arranjo Populacional" in nomeFormatado):
        nomeFormatado = nomeFormatado.replace("Arranjo Populacional", "AP")
    
    nomeFormatado = abreviarNome(nomeFormatado)
    return nomeFormatado

def abreviarNome(nome):
    nomeAbr = nome
    if("AP" in nome or "API" in nome):
        if(len(nomeAbr[1:].split(" "))>3):
            listaNome = nomeAbr.split(' ')
            nomeAbr = listaNome[0]+" "+''.join([f"{n[0]}." for n in listaNome[1:-3]]) +" "+ ' '.join(listaNome[-3:])
    else:
        if(len(nomeAbr.split(" "))>3):
            listaNome = nomeAbr.split(' ')
            nomeAbr = ''.join([f"{n[0]}." for n in listaNome[:-3]]) +" "+ ' '.join(listaNome[-3:])

    return nomeAbr