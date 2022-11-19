from turtle import width
import plotly.graph_objects as go



# Chave de acesso MapBox 
mapbox_access_token = 'pk.eyJ1IjoibmF0YWxpYW9saXZlaXJhIiwiYSI6ImNrd25sd3Q0NTBxcnoyb3ByYXNodTl0dGkifQ.MeGjMDVrvJXxj1zS6MfeHQ'



def carregarMapa(dfRecomendacao, dfCamadas, atributo):

    fig = go.Figure()

    source_to_dest = zip(dfRecomendacao["latitude_ori"], dfRecomendacao["latitude_dest"],
                        dfRecomendacao["longitude_ori"], dfRecomendacao["longitude_dest"],
                        dfRecomendacao["fluxo"])

    #dfCamadas['text'] = 'Municipio: ' + dfCamadas['nome_mun'] + '<br>'+ atributo + ':' + str(dfCamadas[atributo])
    
    #text = ['Municipio: ' + nome + '<br>' + atributo + ':' + str(atr) for nome, atr in zip(listaNome, listaPib)]
    #camada_hover_data = ['Municipio: ' + nome + '<br>' + atributo + ':' + str(atr) for nome, atr in zip(listaNome, listaPib)]

    #dfCamadas['text'] = camada_hover_data
    #print(dfCamadas)

    teste = len(dfRecomendacao["fluxo"])*2
    ## Loop thorugh each flight entry to add line between source and destination
    for slat, dlat, slon, dlon, score in source_to_dest:
        fig.add_trace(go.Scattermapbox(
                            lat = [slat,dlat],
                            lon = [slon, dlon],
                            mode = 'lines',
                            line = dict(width = score*teste, color = '#FF971D')
                            ))

    ## Logic to create labels of source and destination cities of flights
    cities = dfRecomendacao["nome_ori"].values.tolist()+dfRecomendacao["nome_dest"].values.tolist()
    scatter_hover_data = ['Municipio Origem: ' + str(city) for city in zip(cities)]
    
    fig.add_trace(
            go.Scattermapbox(
                        lon = dfRecomendacao["longitude_ori"].values.tolist()+dfRecomendacao["longitude_dest"].values.tolist(),
                        lat = dfRecomendacao["latitude_ori"].values.tolist()+dfRecomendacao["latitude_dest"].values.tolist(),
                        hoverinfo = 'text',
                        text =  scatter_hover_data,
                        mode = 'markers',
                        marker = dict(size = 10, color = '#FFFFFF')),
        )


    listaPib = dfCamadas[atributo].values.tolist()
    listaNome = dfCamadas['nome_mun'].values.tolist()
    camada_hover_data = ['Municipio: ' + nome + '<br>' +  '<br>' +atributo + ':' + str(atr) for nome, atr in zip(listaNome, listaPib)]
    dfCamadas['text'] = camada_hover_data
    print(camada_hover_data)
    ## Loop thorugh each flight entry to plot source and destination as points.
    

    source_to_camadas = zip(dfCamadas["cod_mun"], dfCamadas["nome_mun"],
                        dfCamadas["latitude"], dfCamadas["longitude"])


    for key, value in dfCamadas["text"].items():
        #print(value)
        value = dfCamadas["text"]
        print(value)
        fig.add_trace(
            go.Scattermapbox(
                        lon = dfCamadas["longitude"].values.tolist(),
                        lat = dfCamadas["latitude"].values.tolist(),
                        hoverinfo = 'text',
                        text =  value,
                        mode = 'markers',
                        marker = dict(size = 10, color = '#FF971D', opacity=0.2,)),
        )
        
      
    
    ## Update graph layout to improve graph styling.
    fig.update_layout(
        height=750,
        autosize=True,
        hovermode='closest',
        paper_bgcolor='rgba(0,0,0,0)',
        mapbox={
            'accesstoken':mapbox_access_token,
            'bearing':0,
            'center':{"lat": -14.23500, "lon": -51.92528},
            'pitch':0,
            'zoom':3,
            'style':'dark',
            },
        margin = dict(l = 0, r = 0, t = 0, b = 0)
    )

    fig.layout.update(showlegend=False)
    fig.update_layout(modebar_remove='zoomInMapbox')

    return fig

