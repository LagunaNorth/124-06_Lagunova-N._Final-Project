import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table
import assets.page_styles as ps


def create_layout ():
    return dbc.Container([
        html.Div([
            html.H1('Анализ рынка услуги защиты от DDoS-атак', className='main.header'),
            html.H3('Регион исследования: Санкт-Петербург и Ленинградская область', className='main-subheader')
        ],className='header'),
        dbc.Row([           #Filters
            dbc.Col([html.Label('Услуга Anti-DDoS: Показать', className='filter-label'),
                     dcc.Dropdown(id='provider',
                                  options=[{'label':'только компании, предоставляющие услугу', 'value': 1},
                                            {'label':'только не предоставляющие услугу компании', 'value':0},
                                            {'label': 'все компании', 'value': 3}],
                                            value=3,
                                            clearable=False,
                                            className='filter-dropdown',
                                            style=ps.DROPDOWN_STYLE)],md=6, xs=12),
            dbc.Col([html.Label('Количество AS: Показать компании, у которых', className='filter-label'),
                     dcc.Dropdown(id='AS-count',
                                  options=[{'label':'только 1 AS', 'value': 1},
                                            {'label':'более 1 AS', 'value': 2},
                                            {'label': 'Показать все компании', 'value': 3}],
                                            value=3,
                                            clearable=False,
                                            className='filter-dropdown',
                                            style=ps.DROPDOWN_STYLE)],md=6, xs=12)
            ], class_name='filters-row'),
        dbc.Row([           #Markets_graph
            dbc.Col([dcc.Graph(id='markets_graph', className='dash-graph')], md=12, xs=12)], className='graph-row'),
        dbc.Row([           
            dbc.Col([dcc.Graph(id='business_cat_graph', className='dash-graph')], md=6, xs=12),    #Business_cat_graph
            dbc.Col([dcc.Graph(id='customers_hist', className='dash-graph')], md=6, xs=12)], className='graph-row'),  #Customers_graph
        html.Div([
            html.H3('Статистика по выбранным компаниям', className='stat-header')]),
        dbc.Row([
            dbc.Col([
                dbc.Card(id='total-companies', body=True, class_name='stat-card')
            ], md=4, xs=12),
            dbc.Col([
                dbc.Card(id='total-b2o', body=True, class_name='stat-card')
            ], md=4, xs=12),
            dbc.Col([
                dbc.Card(id='total-customers', body=True, class_name='stat-card')
            ], md=4, xs=12)
        ]),

        html.Div(id='table', className='contacts')
], fluid=True)