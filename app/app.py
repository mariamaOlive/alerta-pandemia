# Libraries imports
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

# Model imports
import camada_model.ctrl_recomendacao as sr
import camada_model.ctrl_info_loader as il

# Visualizações imports
import visualizacao.vis_mapa as vis

# Carregando Model classes
ctrlRecomedacao = sr.CtrlRecomendacao()
ctrlInfoLoader = il.CtrlInfoLoader()

# Carregando dados iniciais
dicEstados = ctrlInfoLoader.dfEstados.to_dict('records')
dicCidades = ctrlInfoLoader.carregarCidadesPorEstado(dicEstados[0]['cod_uf']).to_dict('records')


# Inicializando aplicacao
app = Dash(__name__)

##############################################
#######     Application Layout      ##########
##############################################

app.layout = html.Div(children=[
    html.H1(children='Alerta Epidemia'),

    html.Div([

        # Dropdown-Estado
        html.Div([
            dcc.Dropdown(
                options=[{'label': i['nome_uf'], 'value': i['cod_uf']}
                         for i in dicEstados],
                value=dicEstados[0]['cod_uf'],
                id='dropdown-estado'
            )
        ], className="menu__dropdown"),

        # Dropdown-Cidade
        html.Div(
        id="div-dropdown-cidade", className="menu__dropdown"
    )], id='menu'),

    #Checkboxes
    dcc.Checklist(['Fluxo Rodoviário', 'Fluxo Aéreo'],['Fluxo Rodoviário', 'Fluxo Aéreo'], id='checkbox-fluxo'),

    #Visualização Mapa
    dcc.Graph(
        id='visualizacao'
    ),

    html.Div(id='my-output')
])

#TODO: Remover essa funcao depois, isso eh so para TESTES
def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

##############################################
############     Callbacks      ##############
##############################################

# Callback - Update dropdown de Cidades
@app.callback(
    Output('div-dropdown-cidade', 'children'),
    Input('dropdown-estado', 'value'))
def updateDropdownCidade(idEstado):

    dicCidades = ctrlInfoLoader.carregarCidadesPorEstado(idEstado).to_dict('records')

    dropdownCidades = dcc.Dropdown(
        options=[{'label': i['nome_mun'], 'value': i['cod_mun']} for i in dicCidades],
        value=dicCidades[0]['cod_mun'],
        id='dropdown-cidade'
    )
    return dropdownCidades


# Callback - Busca recomendação da cidade
@app.callback(
    Output('visualizacao', 'figure'),
    Input('dropdown-cidade', 'value'))
def updateRecomendacaoCidade(idCidade):
    print(idCidade)
    dfRecomendacao = ctrlRecomedacao.calculoRecomendacao(idCidade)
    return vis.carregarMapa(dfRecomendacao)

#TODO: Remover depois dos testes --> Callback print Dataframe
@app.callback(
    Output('my-output', 'children'),
    Input('dropdown-cidade', 'value'))
def updateRecomendacaoCidade(idCidade):
    print(idCidade)
    dfRecomendacao = ctrlRecomedacao.calculoRecomendacao(idCidade)
    return generate_table(dfRecomendacao)

#Callback - Seleção de Fluxo
# @app.callback(
#     Output('my-output', 'children'),
#     Input('checkbox-fluxo', 'value'))
# def updateRecomendacaoCidade(idCidade):
#     print(idCidade)
#     dfRecomendacao = ctrlRecomedacao.calculoRecomendacao(idCidade)
#     return generate_table(dfRecomendacao)

if __name__ == '__main__':
    app.run_server(debug=True)
