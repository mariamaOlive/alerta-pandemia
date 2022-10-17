from turtle import width
import plotly.graph_objects as go
import visualizacao.entrada as entrada

entrada = entrada.initialize_data()

# Chave de acesso MapBox 
mapbox_access_token = 'pk.eyJ1IjoibmF0YWxpYW9saXZlaXJhIiwiYSI6ImNrd25sd3Q0NTBxcnoyb3ByYXNodTl0dGkifQ.MeGjMDVrvJXxj1zS6MfeHQ'


# url = urllib.request.urlopen('https://raw.githubusercontent.com/fititnt/gis-dataset-brasil/master/municipio/geojson/municipio.json')
# url.info().get_charset() is None
# url.read().decode('latin1')


# with urlopen('https://raw.githubusercontent.com/fititnt/gis-dataset-brasil/master/municipio/geojson/municipio.json') as response:
#         municipios = json.load(response).decode(errors='replace')


# Read all municipalities in the country at a given year
# mun = read_municipality(code_muni="all", year=2020)

def carregarMapa(listaPath):

    fig = go.Figure()

    # source_to_dest = zip(dfAtributosCidades["latitude"], dfAtributosCidades["nome_mun"],
    #                     dfAtributosCidades["longitude"], dfAtributosCidades["densidade_2021"],
    #                     dfAtributosCidades["indice_atracao"])

    # dfAtributosCidades['text'] = 'Municipio: ' + dfAtributosCidades['nome_mun'] + '<br>Densidade Populacional: ' + (dfAtributosCidades['densidade_2021']).astype(str) +'<br>Indice Atração: ' + dfAtributosCidades['indice_atracao'].astype(str)  +  '<br>PIB: ' + dfAtributosCidades['pib'].astype(str)

    # fig.add_trace(
    #      go.Scattermapbox(
    #                  lon = dfAtributosCidades["longitude"],
    #                  lat = dfAtributosCidades["latitude"],
    #                  mode = 'markers',
    #                  marker = dict(size = dfAtributosCidades['indice_atracao']/50000),
    #                  text = dfAtributosCidades['text'],  
    #                  marker_color = dfAtributosCidades['densidade_2021'],),
    # )

    # # fig = go.Figure(go.Choroplethmapbox(geojson=mun, locations=dfAtributosCidades.densidade_2021, z=dfAtributosCidades.indice_atracao,
    # #                                 colorscale="Viridis", zmin=0, zmax=12,
    # #                                 marker_opacity=0.5, marker_line_width=0))
       
    
    
    for caminho in listaPath:
        caminho_lat =[]
        caminho_lon = []
        nome_municipio = []
        print(caminho.probabilidade)
        for pontos_caminho in caminho.path:
            print(type(pontos_caminho))
            caminho_lat.append(pontos_caminho.latitude)
            caminho_lon.append(pontos_caminho.longitude)
            nome_municipio.append(pontos_caminho.nome)
        fig.add_trace(go.Scattermapbox(
        mode="markers+lines",
        lon=caminho_lon,
        lat=caminho_lat,
        text=nome_municipio,
        marker={'size': 10}))

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
        margin = dict(l = 0, r = 0, t = 0, b = 0),
    )

    fig.update_layout(modebar_remove='zoomInMapbox')

    fig.update_layout(legend_title_text='Rotas - Nós')

#     fig.update_layout(legend=dict(
#     orientation="h",
#     yanchor="bottom",
#     y=1.02,
#     xanchor="right",
#     x=1
# ))

    return fig