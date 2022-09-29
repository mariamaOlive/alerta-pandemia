# Libraries imports
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

# Model imports
from camada_model.ctrl_fluxo import CtrlFluxo
from camada_model.ctrl_info_loader import CtrlInfoLoader
from camada_model.ctrl_atributos_cidade import CtrlAtributosCidade

# Visualizações imports
import visualizacao.vis_mapa as vis

# Carregando Model classes
ctrlFluxo = CtrlFluxo()
ctrlInfoLoader = CtrlInfoLoader()
ctrlAtrCidade = CtrlAtributosCidade()

# Carregando dados iniciais
dicEstados = ctrlInfoLoader.dfEstados.to_dict('records')
dicCidades = ctrlInfoLoader.carregarCidadesPorEstado(dicEstados[0]['cod_uf']).to_dict('records')


# Inicializando aplicacao
app = Dash(__name__)


##############################################
#######    Componetes do Layout     ##########
##############################################

#Componente RadioButtons do tipos de Fluxo
radioButtonsFluxo = dcc.RadioItems(
        options={
        'fluxo_geral': 'Fluxo Rodoviário + Aéreo',
        'fluxo_aereo': 'Fluxo Aéreo',
        'fluxo_rodo': 'Fluxo Rodoviário'
        },
        value='fluxo_geral', id='checkbox-fluxo')


    #Componente dos drops de Estados
dropDownEstados = html.Div([

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
        id="div-dropdown-cidade", className="menu__dropdown"
    )], id='menu')

#Componente que contem a visualização do mapa
containerMapa = dcc.Graph(id='visualizacao')

#TODO: Remover após testes
containerDf = html.Div(id='my-output')

#Componente da tab de Fluxo 
tabFluxo = html.Div([
        dropDownEstados, 
        radioButtonsFluxo, 
        containerMapa,
        containerDf
])

#Componente da tab de Atributos 
tabAtributos = html.Div([
        containerDf
])


##############################################
#######     Application Layout      ##########
##############################################

app.layout = html.Div(children=[
    #Título da aplicacao
    html.H1(children='Alerta Epidemia'),

    #Tabs da aplicação 
    dcc.Tabs(id="tabs-vis", value='tab-fluxo', children=[
        dcc.Tab(label='Fluxo', value='tab-fluxo'),
        dcc.Tab(label='Atributos gerais', value='tab-atributos'),
    ]),

    #Container das tabs da aplicação
    html.Div(id='tabs-content')
]
)


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

# Callback - Carregar conteúdo de cada tab
@app.callback(Output('tabs-content', 'children'),
              Input('tabs-vis', 'value'))
def render_content(tab):
    if(tab == "tab-fluxo"):
        return tabFluxo
    elif(tab == "tab-atributos"):
        df = ctrlAtrCidade.carregarTodasCidades()

        return generate_table(df)


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
    Input('dropdown-cidade', 'value'),
    Input('checkbox-fluxo', 'value'))
def updateRecomendacaoCidade(idCidade, tipoFluxo):
    print(tipoFluxo)
    #Funcao com as infos da cidade de origem 
    infoCidade, dfFluxo = ctrlFluxo.percentualFluxo(idCidade, tipoFluxo)

    return vis.carregarMapa(dfFluxo)


#TODO: Remover depois dos testes --> Callback print Dataframe
#Callback - Seleção de Fluxo - Rodoviário/Aéreo
@app.callback(
    Output('my-output', 'children'),
    Input('dropdown-cidade', 'value'),
    Input('checkbox-fluxo', 'value'))
def updateRecomendacaoCidade(idCidade, tipoFluxo):
    print(tipoFluxo)

    infoCidade, dfFluxo = ctrlFluxo.percentualFluxo(idCidade, tipoFluxo)
    return generate_table(dfFluxo)

if __name__ == '__main__':
    app.run_server(debug=True)
