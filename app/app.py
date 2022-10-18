# Libraries imports
from dash import Dash, html, dcc, Input, Output, State, ctx
import dash
import plotly.express as px
import pandas as pd


# Model imports
from camada_model.ctrl_fluxo import CtrlFluxo
from camada_model.ctrl_info_loader import CtrlInfoLoader
from camada_model.ctrl_atributos_cidade import CtrlAtributosCidade
from camada_model.ctrl_spreaders import CtrlSpreader


# Visualizações imports
import visualizacao.vis_mapa as vis
import visualizacao.vis_mapa_2 as vis_2
import visualizacao.vis_bar_chart as visBarchart

# Carregando Model classes
ctrlFluxo = CtrlFluxo()
ctrlInfoLoader = CtrlInfoLoader()
ctrlAtrCidade = CtrlAtributosCidade()
ctrlSpreader = CtrlSpreader()

# Carregando dados iniciais
dicEstados = ctrlInfoLoader.dfEstados.to_dict('records')
dicCidades = ctrlInfoLoader.carregarCidadesPorEstado(dicEstados[0]['cod_uf']).to_dict('records')

#Variáveis de estado
tabSelecionada = "fluxo_geral"

# Inicializando aplicacao
app = Dash(__name__)


##############################################
#######    Componetes do Layout     ##########
##############################################

#Componente RadioButtons do tipos de Fluxo
radioBtnFluxoTrans = dcc.RadioItems(
        options={
        'fluxo_geral': 'Fluxo Rodoviário + Aéreo',
        'fluxo_aereo': 'Fluxo Aéreo',
        'fluxo_rodo': 'Fluxo Rodoviário'
        },
        value='fluxo_geral', id='radio-fluxo', labelStyle={'display': 'block'})

radioBtnFluxoSaude = dcc.RadioItems(
        options={
        'saude_alta': 'Alta complexidade',
        'saude_baixa_media': 'Baixa e média complexidade',
        },
        value='saude_alta', id='radio-fluxo', inline=False)

#Dropdown com atributos variados
dropdownAtributos = html.Div([
                html.Label("Adicione camadas de visualização", className="dropdown-ctn-text"),
                dcc.Dropdown(
                options=[
                {"label":"PIB", "value":"pib"},
                {"label":"Densidade populacional", "value":"densidade_2021"},
                {"label":"Hierarquia", "value":"hierarquia"},
                {"label":"Índice de atração", "value":"indice_atracao"}, 
                {"label":"IA saúde Baixa/Média", "value":"ia_saude_bm"},
                {"label":"IA saúde Alta", "value":"ia_saude_a"},
                {"label":"IA aeroportos", "value":"ia_aeroporto"},
                {"label":"IA transportes", "value":"ia_transporte"},
                {"label":"Leitos/mil hab.", "value":"num_leitos"},
                {"label":"Rede Sentinela", "value":"sentinela"}
                ],
                id='dropdown-atributos',
                multi=True)
    ], id = 'dropdown-atributos-container')


#Componente do drop de Estados
dropDownsFluxo= html.Div([
        # Dropdown-Estado
        html.Div([
            html.P("Estado", className="dropdown-ctn-text"),
            dcc.Dropdown(
                options=[{'label': i['nome_uf'], 'value': i['cod_uf']}
                        for i in dicEstados],
                value=dicEstados[0]['cod_uf'],
                id='dropdown-estado'    
            )
        ], className="menu__dropdown"),

         # Dropdown-Analise
        html.Div([
            html.P("Nível de Análise", className="dropdown-ctn-text"),
            dcc.Dropdown(
                options=[
                {"label":"Cidade", "value":"cidade"},
                {"label":"Região de Saúde", "value":"regiao"}
                ],
                value="cidade",
                id='dropdown-analise'
            )
        ], className="menu__dropdown"),

        # Dropdown-Dinâmico
        html.Div(id="div-dropdown-dinamico", className="menu__dropdown")
], id='menu')

#Componente que contem a visualização do mapa
containerMapa = dcc.Graph(id='visualizacao', className='visualizacao-mapa')
containerMapa_2 = dcc.Graph(id='visualizacao_2', className='visualizacao-mapa')

#Componente visualizacao lateral
containerVisLateral = html.Div([
    html.Div("", id="vis_lateral", className="small_container-vis"),
    html.Div("TODO: EXPLICAÇÃO DOS FLUXOS, ATRIBUTOS, CÁLCULOS ETC", id="vis_explicacao", className="small_container-vis")
    ]
    , id="vis_lat-container")

#TODO: Remover após testes
containerDf = html.Div(id='my-output')
containerDf_2 = html.Div(id='my-output-2')

#Funcao que gera o dropdown do numeroMax de cidades mostradas
def generateDropdown(numMaxCidades=20):

    opcoesDropdown = [i for i in range(0, numMaxCidades+1)]
    numeroDefault = numMaxCidades if numMaxCidades<20 else 20
    print("opcoes ", opcoesDropdown)
    print("numeroMaxCidades ", numMaxCidades)

    return [html.Label("Número de conexões", className="dropdown-ctn-text"),
            dcc.Dropdown(options=opcoesDropdown,value=numeroDefault,id='dropdown-numero')]

#Componente da tab de Fluxo Transporte
def criarComponentesTabFluxo(tipoFluxo):

    componenteFluxo = radioBtnFluxoTrans if tipoFluxo=="transporte" else radioBtnFluxoSaude
    dropdownNumero = html.Div(generateDropdown(),id="container-dropdown-numero")

    tabFluxo = html.Div([
        html.Div([
            containerMapa,
            html.Div([componenteFluxo,dropdownAtributos, dropdownNumero], id="mapa-selecao-container")
            ], id="vis-container"),   

        containerVisLateral,
        # containerDf
    ])

    return tabFluxo


#Componente da tab de Atributos 
tabAtributos = html.Div([
            html.Div([
                containerMapa_2,
                html.Div([dropdownAtributos], id="mapa-selecao-container")
                ], id="vis-container"),   
                        
            containerVisLateral,
            # containerDf
], id="tab-atributos")

##############################################
#######     Application Layout      ##########
##############################################

app.layout = html.Div(children=[

    html.Div(id="top-container", children=[
        #Título da aplicacao
        html.Div(id = "title-container",
            children = [html.H1(children='Alerta Epidemia', id = "app-title")]
        ),

        #Dropdown Estado/Nivel analise/Cidade ou Regiao 
        dropDownsFluxo
    ]),
    
    #Tabs da aplicação 
    dcc.Tabs(id="tabs-vis", value='tab-fluxo-transporte', children=[
        dcc.Tab(label='Fluxo de transporte', value='tab-fluxo-transporte', className="tab-parte"),
        dcc.Tab(label='Fluxo serviços de saúde', value='tab-fluxo-saude', className="tab-parte"),
        dcc.Tab(label='Análise de propagação', value='tab-atributos', className="tab-parte")
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

############     Callbacks: Geral      ##############

# Callback - Carregar conteúdo de cada tab
@app.callback(Output('tabs-content', 'children'),
              Input('tabs-vis', 'value'))
def render_content(tab):
    global tabSelecionada
    tabSelecionada = tab
    
    if(tab == "tab-fluxo-transporte"):
        return criarComponentesTabFluxo("transporte")
    elif(tab == "tab-fluxo-saude"):
        return criarComponentesTabFluxo("saude")   
    elif(tab == "tab-atributos"):
        return tabAtributos  

############     Callbacks: Tab Fluxo de Transporte + Tab Saúde     ##############

# Callback - Update dropdown dinamico
@app.callback(
    Output('div-dropdown-dinamico', 'children'),
    Input('dropdown-estado', 'value'), 
    Input('dropdown-analise', 'value'))
def updateDropdownCidade(idEstado, tipoDropdown):
    if tipoDropdown == "cidade":
        return carregarDropdownCidades(idEstado)
    elif tipoDropdown == "regiao":
        return carregarDropdownRegiao(idEstado)

#Funcao de apoio de carregamento de dropdown
def carregarDropdownCidades(idEstado):
    dicCidades = ctrlInfoLoader.carregarCidadesPorEstado(idEstado).to_dict('records')
    return [
            html.P("Cidade", className="dropdown-ctn-text"),
            dcc.Dropdown(
                options=[{'label': i['nome_mun'], 'value': i['cod_mun']} for i in dicCidades],
                value=dicCidades[0]['cod_mun'],
                id='dropdown-cid_reg'
            )]

#Funcao de apoio de carregamento de dropdown
def carregarDropdownRegiao(idEstado):
    dicRegiao = ctrlInfoLoader.carregarRegioesPorEstado(idEstado).to_dict('records')
    return [
        html.P("Região de Saúde", className="dropdown-ctn-text"),
        dcc.Dropdown(
            options=[{'label': i['nome_reg_saude'], 'value': i['cod_reg_saude']} for i in dicRegiao],
            value=dicRegiao[0]['cod_reg_saude'],
            id='dropdown-cid_reg'
    )]


# Callback - Renderiza fluxo de transporte da cidade
@app.callback(
    [Output('visualizacao', 'figure'),
    Output('container-dropdown-numero', 'children')],
    [State('dropdown-analise', 'value')],
    [Input('dropdown-cid_reg', 'value'),
    Input('radio-fluxo', 'value'),
    Input('dropdown-numero', 'value')]
    )
def updateFluxo(tipoAnalise,id, tipoFluxo, numeroCidades):
    print("Entrei aqui danado")
    triggered_id = ctx.triggered_id

    if triggered_id == "dropdown-numero":
        numeroMaxCidades, visualizacao = updateFluxoTipo(tipoAnalise, id, tipoFluxo, numeroCidades)  
        return visualizacao, dash.no_update
    else:
        numeroMaxCidades, visualizacao = updateFluxoTipo(tipoAnalise, id, tipoFluxo)
        return visualizacao, generateDropdown(numeroMaxCidades)

def updateFluxoTipo(tipoAnalise, id, tipoFluxo, numeroCidades=20):
    if tipoAnalise == 'cidade':
            return updateFluxoCidade(id, tipoFluxo, numeroCidades)
    elif tipoAnalise == 'regiao':
            return updateFluxoRegiao(id, tipoFluxo, numeroCidades)  

def updateFluxoCidade(idCidade, tipoFluxo, numeroCidades=20):
    infoCidade, dfFluxo = ctrlFluxo.percentualFluxo(idCidade, tipoFluxo)
    visualizacao = vis.carregarMapa(dfFluxo[:numeroCidades])

    visualizacaoBarchart = visBarchart.carregaBarChart(dfFluxo)
    #Retorna a numero de ligacoes e visualizacao 
    return dfFluxo.shape[0],visualizacao,visualizacaoBarchart
     
def updateFluxoRegiao(idRegiao, tipoFluxo, numeroCidades=20):
    infoCidade, dfFluxo = ctrlFluxo.percentualFluxo(2611606, tipoFluxo)
    visualizacao = vis.carregarMapa(dfFluxo[:numeroCidades])
    #Retorna a numero de ligacoes e visualizacao 
    return dfFluxo.shape[0],visualizacao
 

############     Callbacks: Tab Atributos     ##############

# Callback - Renderiza diversos atributos da cidade
@app.callback(
    Output('visualizacao_2', 'figure'),
    Input('tab-atributos', 'children'),
    Input('dropdown-cid_reg', 'value'))
def updateAtributosCidades(tabvalue, id):
    listaPath = ctrlSpreader.buscarSpreaders(id)
    return vis_2.carregarMapa(listaPath)



if __name__ == '__main__':
    app.run_server(debug=True)
