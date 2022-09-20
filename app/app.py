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
app.title = 'Alerta Epidemia'

##############################################
#######     Application Layout      ##########
##############################################

app.layout = html.Div(
    children=[
        html.Div(
            className="header",
            children=[
                html.H1("Alerta Epidemia", className="header__text"),
            ],
    ),

    html.Section([
        html.Div([

            # Dropdown-Estado
            html.Div([
                dcc.Dropdown(
                    options=[{'label': i['nome_uf'], 'value': i['cod_uf']}
                            for i in dicEstados],
                    value=dicEstados[0]['cod_uf'],
                    id='dropdown-estado',
                    style={'font-size': 15}
                )
            ], className="menu__dropdown"),

            # Dropdown-Cidade
            html.Div(
            #     [
            #     dcc.Dropdown(
            #         options=[{'label': i['nome_mun'], 'value': i['cod_mun']}
            #                  for i in dicCidades],
            #         value=dicCidades[0]['cod_mun'],
            #         id='dropdown-cidade'
            #     )
            # ], 
            id="div-dropdown-cidade", className="menu__dropdown",
            style={'font-size': 15}
        )], id='menu'),
        html.Div(id='world_line_2'),
        dcc.Graph(
            id='visualizacao'
            
        )
    ]),    
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
    dfRecomendacao = ctrlRecomedacao.calculoRecomendacao(idCidade, 20)
    #return generate_table(dfRecomendacao)
    return vis.carregarMapa(dfRecomendacao)


if __name__ == '__main__':
    app.run_server(debug=True)
