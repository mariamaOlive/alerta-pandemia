from turtle import width
import plotly.graph_objects as go



# Chave de acesso MapBox 
mapbox_access_token = 'pk.eyJ1IjoibmF0YWxpYW9saXZlaXJhIiwiYSI6ImNrd25sd3Q0NTBxcnoyb3ByYXNodTl0dGkifQ.MeGjMDVrvJXxj1zS6MfeHQ'

def carregarMapa(dfAtributosCidades):

    fig = go.Figure()

    source_to_dest = zip(dfAtributosCidades["latitude"], dfAtributosCidades["longitude"],
                        dfAtributosCidades["nome_mun"], dfAtributosCidades["indice_atracao"],dfAtributosCidades["densidade_2021"])

    fig.add_trace(
        go.Scattermapbox(
                    lon = dfAtributosCidades["longitude"],
                    lat = dfAtributosCidades["latitude"],
                    mode = 'markers',
                    marker = dict(size = 10)),
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
    )

    fig.update_layout(modebar_remove='zoomInMapbox')

    return fig