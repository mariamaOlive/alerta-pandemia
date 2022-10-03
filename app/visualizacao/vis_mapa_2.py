from turtle import width
import plotly.graph_objects as go




# Chave de acesso MapBox 
mapbox_access_token = 'pk.eyJ1IjoibmF0YWxpYW9saXZlaXJhIiwiYSI6ImNrd25sd3Q0NTBxcnoyb3ByYXNodTl0dGkifQ.MeGjMDVrvJXxj1zS6MfeHQ'

def carregarMapa(dfAtributosCidades):

    fig = go.Figure()

    dfAtributosCidades['text'] = dfAtributosCidades['nome_mun'] + '' + ', ' + 'Indice Atração: ' + dfAtributosCidades['indice_atracao'].astype(str)  + '' + ', '+ 'PIB: ' + dfAtributosCidades['pib'].astype(str)

    fig.add_trace(
         go.Scattermapbox(
                     lon = dfAtributosCidades["longitude"],
                     lat = dfAtributosCidades["latitude"],
                     mode = 'markers',
                     marker = dict(size = 10),
                     text = dfAtributosCidades['text'],  
                     marker_color = dfAtributosCidades['densidade_2021'],),
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

    fig.update_layout(modebar_remove='zoomInMapbox')

    return fig