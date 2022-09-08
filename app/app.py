#Libraries imports
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

#Model imports
import camada_model.sistema_recomendacao as sr
import camada_model.info_loader as il

#Carregando Model classes 
sistemaRecomendacao =  sr.SistemaRecomendacao()
infoLoader = il.InfoLoader()

#Inicializando aplicacao
app = Dash(__name__)


##############################################
#######     Application Layout      ##########
##############################################

app.layout = html.Div(children=[
    html.H1(children='Alerta Epidemia'),
    
    html.Div([

        #Dropdown-State
        html.Div([
            dcc.Dropdown(
                infoLoader.dfEstados["nome_uf"],
                'Estado',
                id='dropdown-estado'
            )
        ], className="menu__dropdown"),

        #Dropdown-City
        html.Div([
            dcc.Dropdown(
                ['New York City', 'Montréal', 'San Francisco'],
                'Município',
                id='dropdown-cidade'
            )
        ], id = "div-dropdown-cidade", className="menu__dropdown"
        ) 
        
    ], id = 'menu')
])


##############################################
############     Callbacks      ##############
##############################################

# Callback - Dropdown menu
# @app.callback(
#     Output('map-graphic', 'figure'),
#     Input('dropdown-state', 'value'),
#     Input('dropdown-city', 'value'))
# def update_graph(state_name, city_name):
#     pass
#     return fig


if __name__ == '__main__':
    app.run_server(debug=True)
