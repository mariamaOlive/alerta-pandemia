from turtle import width
import plotly.graph_objects as go


# Chave de acesso MapBox 
mapbox_access_token = 'pk.eyJ1IjoibmF0YWxpYW9saXZlaXJhIiwiYSI6ImNrd25sd3Q0NTBxcnoyb3ByYXNodTl0dGkifQ.MeGjMDVrvJXxj1zS6MfeHQ'

def carregarMapa(dfRecomendacao):

    fig = go.Figure()

    source_to_dest = zip(dfRecomendacao["latitude_ori"], dfRecomendacao["latitude_dest"],
                        dfRecomendacao["longitude_ori"], dfRecomendacao["longitude_dest"],
                        dfRecomendacao["fluxo"])

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
    #countries = df_sample["Pais.Origem"].values.tolist()+df_sample["Pais.Destino"].values.tolist()
    scatter_hover_data = [city for city in zip(cities)]

    ## Loop thorugh each flight entry to plot source and destination as points.
    fig.add_trace(
        go.Scattermapbox(
                    lon = dfRecomendacao["longitude_ori"].values.tolist()+dfRecomendacao["longitude_dest"].values.tolist(),
                    lat = dfRecomendacao["latitude_ori"].values.tolist()+dfRecomendacao["latitude_dest"].values.tolist(),
                    hoverinfo = 'text',
                    text = scatter_hover_data,
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