from dash import Dash, dash_table
import plotly.graph_objects as go
import pandas as pd

def carregaTable(df):
    dfTable = df

    fig = go.Figure(data=[go.Table(
    header=dict(values=list(dfTable.columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[dfTable.nome_mun, dfTable.uf, dfTable.populacao_2021, dfTable.pib, dfTable.indice_atracao, dfTable.rede_sentinela],
               fill_color='lavender',
               align='left'))])

    return fig
