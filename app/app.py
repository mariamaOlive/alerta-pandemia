# Libraries imports
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

# Model imports
import camada_model.ctrl_recomendacao as sr
import camada_model.ctrl_info_loader as il

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
        #     [
        #     dcc.Dropdown(
        #         options=[{'label': i['nome_mun'], 'value': i['cod_mun']}
        #                  for i in dicCidades],
        #         value=dicCidades[0]['cod_mun'],
        #         id='dropdown-cidade'
        #     )
        # ], 
        id="div-dropdown-cidade", className="menu__dropdown"
    )], id='menu'),
    html.Div(id='my-output')
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
    Output('my-output', 'children'),
    Input('dropdown-cidade', 'value'))
def updateRecomendacaoCidade(idCidade):
    print("test 1")
    print(idCidade)
    listaCidades = ctrlRecomedacao.calculoRecomendacao(idCidade)
    return f"{listaCidades}"


if __name__ == '__main__':
    app.run_server(debug=True)
