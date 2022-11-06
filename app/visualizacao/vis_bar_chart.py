import plotly.express as px

def carregaBarChart(df):

    dfBarChart = df.head(5)

    fig = px.bar(dfBarChart, 
     x="fluxo", y="nome_dest", orientation='h', text_auto=True,
     color_discrete_sequence=px.colors.qualitative.Pastel[1:], template="plotly_dark",
     labels={'fluxo':'Fluxos', 'nome_dest':'Destino'},
        ).update_layout(margin={"r":0,"t":46,"l":0,"b":6}).update_xaxes(visible=True).update_xaxes(title_text='Fluxos').update_traces(texttemplate='%{x:.d}')

    fig.update_layout(title_text='Os Maiores Fluxos', title_x=0.5)

    fig.update_traces(marker_color='rgb(255, 151, 29)', marker_line_color='rgb(255, 255, 255)',
                  marker_line_width=1.5)
 
    return fig
