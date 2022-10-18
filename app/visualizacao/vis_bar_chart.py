import plotly.express as px

def carregaBarChart(df):

    fig = px.bar(df, x="fluxo", y="nome_dest", orientation='h')

    return fig
