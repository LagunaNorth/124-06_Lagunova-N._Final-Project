import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px
from dash import Input, Output, html, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
from db.db import df
import assets.page_styles as ps


pio.templates['custom'] = pio.templates['plotly'].update(
    layout=dict(colorway=ps.MY_PALETTE))
pio.templates.default = 'custom'

def register_callbacks (app):
    @app.callback(
            Output("markets_graph", "figure"),
            Output("business_cat_graph", "figure"),
            Output("customers_hist", "figure"),
            Output('total-companies', 'children'),
            Output('total-b2o', 'children'),
            Output('total-customers', 'children'),
            Output('table', 'children'),
            Input("provider", "value"),
            Input("AS-count", "value"),
            )
    def update_graphs(provider, numbersOfAS): 

        seg_counts = df['сегмент рынка'].value_counts() 
        for_others = 10 
        other_seg = seg_counts[seg_counts < for_others].index 
        mapping = {cat: 'Прочие' for cat in other_seg} 
        df['сегменты рынка'] = df['сегмент рынка'].map(mapping).fillna(df['сегмент рынка'])
        
        if provider == 0 and numbersOfAS == 1:
            filtered_df = df[(df['предоставляет услугу'] == 'не предоставляет услугу') & (df['кол-во AS'] == 1)]
        elif provider == 0 and numbersOfAS == 2:
            filtered_df = df[(df['предоставляет услугу'] == 'не предоставляет услугу') & (df['кол-во AS'] > 1)]
        elif provider == 0 and numbersOfAS == 3:
            filtered_df = df[(df['предоставляет услугу'] == 'не предоставляет услугу')]
        elif provider == 1 and numbersOfAS == 1:
            filtered_df = df[(df['предоставляет услугу'] == 'предоставляет услугу') & (df['кол-во AS'] == 1)]
        elif provider == 1 and numbersOfAS == 2:
            filtered_df = df[(df['предоставляет услугу'] == 'предоставляет услугу') & (df['кол-во AS'] > 1)]
        elif provider == 1 and numbersOfAS == 3:
            filtered_df = df[(df['предоставляет услугу'] == 'предоставляет услугу')]
        elif provider == 3 and numbersOfAS == 1:
            filtered_df = df[(df['кол-во AS'] == 1)]
        elif provider == 3 and numbersOfAS == 2:
            filtered_df = df[(df['кол-во AS'] > 1)]
        else:
            filtered_df = df

        df_stat = filtered_df
        total_companies = len(df_stat)
        total_b2o = len(df_stat[(df_stat['сегмент рынка'] == 'Телеком')])
        total_cust = len(df_stat[(df_stat['является клиентом'] == 'клиент')])
        percent_total_cust = (total_cust / total_companies) * 100

        market_fig = go.Figure()
        market_fig.add_trace(
            go.Histogram(x = filtered_df['сегменты рынка'], 
                         name='Сегменты рынка'))
        market_fig.update_layout(
            title='Распределение компаний по сегментам рынка',
            title_font_size=ps.GRAPH_TITLE_FONT_SIZE,
            title_x=ps.GRAPH_TITLE_ALIGN,
            title_font_weight=ps.GRAPH_FONT_WEIGHT,
            title_font_color=ps.GRAPH_TITLE_FONT_COLOR,
            yaxis_title='Кол-во компаний',
            font=dict(family=ps.GRAPH_FONT_FAMILY),
            xaxis=dict(title_font_size=ps.GRAPH_FONT_SIZE, tickfont=dict(size=ps.GRAPH_FONT_SIZE)),
            yaxis=dict(title_font_size=ps.GRAPH_FONT_SIZE, tickfont=dict(size=ps.GRAPH_FONT_SIZE)),
            plot_bgcolor=ps.PLOT_BACKGROUND_COLOR,
            paper_bgcolor=ps.PAPER_BACKGROUND_COLOR,
        )

        business_fig = go.Figure()
        business_fig.add_trace(go.Histogram(x=filtered_df['категория бизнеса'], 
                                      name='Категории бизнеса'))
        business_fig.update_layout(
            title='Распределение компаний по категориям бизнеса',
            title_font_size=ps.GRAPH_TITLE_FONT_SIZE,
            title_x=ps.GRAPH_TITLE_ALIGN,
            title_font_weight=ps.GRAPH_FONT_WEIGHT,
            title_font_color=ps.GRAPH_TITLE_FONT_COLOR,
            yaxis_title='Кол-во компаний',
            font=dict(family=ps.GRAPH_FONT_FAMILY),
            xaxis=dict(title_font_size=ps.GRAPH_FONT_SIZE, tickfont=dict(size=ps.GRAPH_FONT_SIZE)),
            yaxis=dict(title_font_size=ps.GRAPH_FONT_SIZE, tickfont=dict(size=ps.GRAPH_FONT_SIZE)),
            plot_bgcolor=ps.PLOT_BACKGROUND_COLOR,
            paper_bgcolor=ps.PAPER_BACKGROUND_COLOR,
        )
        customers_hist = go.Figure(go.Histogram(
                x=filtered_df['является клиентом'],
                name='клиенты'))
        customers_hist.update_layout(
            title='Распределение клиенты/не клиенты',
            title_font_size=ps.GRAPH_TITLE_FONT_SIZE,
            title_x=ps.GRAPH_TITLE_ALIGN,
            title_font_weight=ps.GRAPH_FONT_WEIGHT,
            title_font_color=ps.GRAPH_TITLE_FONT_COLOR,
            yaxis_title='Кол-во компаний',
            font=dict(family=ps.GRAPH_FONT_FAMILY),
            xaxis=dict(title_font_size=ps.GRAPH_FONT_SIZE, tickfont=dict(size=ps.GRAPH_FONT_SIZE)),
            yaxis=dict(title_font_size=ps.GRAPH_FONT_SIZE, tickfont=dict(size=ps.GRAPH_FONT_SIZE)),
            plot_bgcolor=ps.PLOT_BACKGROUND_COLOR,
            paper_bgcolor=ps.PAPER_BACKGROUND_COLOR,
        )
        card_companies = html.Div([
            html.H5('ВСЕГО НАЙДЕНО:'),
            html.P (f'{total_companies} компаний')
        ])
        card_b2o = html.Div([
            html.H5('ИЗ НИХ ИЗ СЕКТОРА B2O:'),
            html.P (f'{total_b2o}')
        ])
        card_custom = html.Div([
            html.H5('ДОЛЯ НАШИХ КЛИЕНТОВ В ВЫБОРКЕ'),
            html.P (f'{percent_total_cust:.0f}%')
        ])


        contacts = df_stat[['id компании', 'телефон', 'e-mail', 
                            'сегмент рынка', 'категория бизнеса']]
        data = contacts.to_dict('records')
        contacts_columns = [{'name': i, 'id': i} for i in (contacts.columns)]
        table = dbc.Card([
            dbc.CardHeader('Контакты компаний'),
            dbc.CardBody([dash_table.DataTable(id='my-table', 
                                               columns=contacts_columns, 
                                               data=data,
                                               style_table={'overflowX': 'auto', 'color':'#5b55c1'}, 
                                               style_cell={'textAlign': 'left', 'color':'#5b55c1'}, 
                                               style_header={'backgroundColor': '#f7fdfa', 'color':'#5b55c1', 'fontWeight': 'bold'})
                                               ])
        ])
        
        return market_fig, business_fig, customers_hist, card_companies, card_b2o, card_custom, table

