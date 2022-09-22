import plotly.graph_objects as go






# Chave de acesso MapBox 
mapbox_access_token = 'pk.eyJ1IjoibmF0YWxpYW9saXZlaXJhIiwiYSI6ImNrd25sd3Q0NTBxcnoyb3ByYXNodTl0dGkifQ.MeGjMDVrvJXxj1zS6MfeHQ'

def carregarMapa(dfRecomendacao):

    fig = go.Figure()

    source_to_dest = zip(dfRecomendacao["latitude_ori"], dfRecomendacao["latitude_dest"],
                        dfRecomendacao["longitude_ori"], dfRecomendacao["longitude_dest"],
                        dfRecomendacao["fluxo"])

    ## Loop thorugh each flight entry to add line between source and destination
    for slat, dlat, slon, dlon, num_flights in source_to_dest:
        fig.add_trace(go.Scattermapbox(
                            lat = [slat,dlat],
                            lon = [slon, dlon],
                            mode = 'lines',
                            line = dict(width = num_flights/100)
                            ))

    ## Logic to create labels of source and destination cities of flights
    cities = dfRecomendacao["nome_ori"].values.tolist()+dfRecomendacao["nome_dest"].values.tolist()
    ##countries = dfRecomendacao["Pais.Origem"].values.tolist()+dfRecomendacao["Pais.Destino"].values.tolist()
    scatter_hover_data = [city for city in zip(cities)]

    ## Loop thorugh each flight entry to plot source and destination as points.
    fig.add_trace(
        go.Scattermapbox(
                    lon = dfRecomendacao["longitude_ori"].values.tolist()+dfRecomendacao["longitude_dest"].values.tolist(),
                    lat = dfRecomendacao["latitude_ori"].values.tolist()+dfRecomendacao["latitude_dest"].values.tolist(),
                    hoverinfo = 'text',
                    text = scatter_hover_data,
                    mode = 'markers',
                    marker = dict(size = 10, color = 'orangered', opacity=0.1,))
        )

    ## Update graph layout to improve graph styling.
    fig.update_layout(
        mapbox=dict(
            accesstoken=mapbox_access_token, #
            center=go.layout.mapbox.Center(lat=-46.4565518, lon=-13.4008012),
            zoom=4
        )
    )

    return fig