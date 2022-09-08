from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd


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
                ['New York City', 'Montréal', 'San Francisco'],
                'Estado',
                id='dropdown-state'
            )
        ], className="menu__dropdown"),

        #Dropdown-City
        html.Div([
            dcc.Dropdown(
                ['New York City', 'Montréal', 'San Francisco'],
                'Município',
                id='dropdown-city'
            )
        ], id = "div-dropdown-city", className="menu__dropdown"
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
