# -*- coding: utf-8 -*-
import json
from datetime import datetime

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State

from app import app
from apps import common
from apps.data import dataset

colors_dict = {
    "Casos activos": 'info',
    "Infectados": 'danger',
    "Fallecidos": 'primary',
    "Recuperados": 'success',
    "casos_activos_1k": 'info',
    "casos_1k": 'danger',
    "fallecidos_1k": 'primary',
    "recuperados_1k": 'success',
}


with open('geo.json') as response:
    communities = json.load(response)

option_com = []

for comunidad in dataset.hoy['CCAA'].sort_values().unique().tolist():
    option_com.append(
        {'label': comunidad, 'value': comunidad}
    )

cards_content = [dcc.Dropdown(
    id='comunidad-drop',
    options=option_com,
    clearable=False,
    value='Andalucía',
    searchable=False,
    style={'fontSize': '18.75px', 'marginTop': '12px', 'width': '190px'}
)]

for i, (metric, value) in enumerate(dataset.metrics_dict.items()):
    cards_content.append(
        dbc.Card(
            dbc.CardBody(
                [html.H6([metric],
                         className="card-subtitle", style={'marginBottom': '5px'}),
                    html.H4("0", id="val_{}".format(
                        metric), className="card-title"),
                    html.H6(["🠝 0 (24h.)"],
                            className="card-subtitle", id="inc_{}".format(metric)),




                 ]
            ),

            color=colors_dict[metric],
            inverse=True,
            style={'marginTop': "15px", "width": "190px"}
        )
    )


page = dbc.Container(
    [
        common.navbar,
        dbc.Row([
            dbc.Col(cards_content, width=2, style={'position': 'fixed'}),
                dbc.Col([html.H1("Evolución diaria", className="display-5", style={'paddingTop': '15px'}),
                         html.P(
                    "Gráfico histórico temporal de contagios, fallecidos y recuperados con fechas clave destacadas.",
                    className="lead",
                ),
                    html.Hr(className="my-2"),
                    dcc.Graph(
                        id='daily-evolution', style={'marginTop': '15px', 'height': '280px'}, animate=True,
                )], width={"size": 10, "offset": 2})
                ],
                style={"paddingLeft": "10px", 'paddingBottom': '20px'}
                ),

        dbc.Row([
            dbc.Col([html.H1("Incrementos diarios", className="display-5", style={'paddingTop': '15px'}),
                     html.P(
                "Cantidad diaria de cada tipo",
                className="lead",
            ),
                html.Hr(className="my-2"),
                dcc.Graph(
                    id='daily-increment',
                    style={'marginTop': '15px', 'height': '280px'}, animate=True,
            )], width={"size": 10, "offset": 2})
        ],
            style={"paddingLeft": "10px", 'paddingBottom': '20px'}
        )


    ],
    fluid=True,
    style={'padding': '0px', 'backgroundColor': '#d4dadc'}
)


@app.callback(
    Output('daily-evolution', 'figure'), [Input('comunidad-drop', 'value')]
)
def update_daily_evolution(comunidad):
    return {
        'data': [
            {'x': pd.DatetimeIndex(dataset.df[dataset.df['CCAA'] == comunidad]['Fecha']).to_pydatetime(),
             'y': dataset.df[dataset.df['CCAA'] == comunidad]['Casos'], 'type': 'scatter', 'name': 'Casos',  'marker': {'color': 'rgb(39, 128, 227)'}},
            {'x': pd.DatetimeIndex(dataset.df[dataset.df['CCAA'] == comunidad]['Fecha']).to_pydatetime(),
             'y': dataset.df[dataset.df['CCAA'] == comunidad]['Fallecidos'], 'type': 'scatter', 'name': 'Fallecidos', 'marker': {'color': 'rgb(55, 58, 60)'}},
            {'x': pd.DatetimeIndex(dataset.df[dataset.df['CCAA'] == comunidad]['Fecha']).to_pydatetime(),
             'y': dataset.df[dataset.df['CCAA'] == comunidad]['Recuperados'], 'type': 'scatter', 'name': 'Recuperados', 'marker': {'color': 'rgb(63, 182, 24)'}},
            {'x': [datetime.strptime('2020-03-14 00:00', '%Y-%m-%d %H:%M'), datetime.strptime('2020-03-14 00:01', '%Y-%m-%d %H:%M')], 'y': [
                0, dataset.df[dataset.df['CCAA'] == comunidad]['Casos'].max()], 'type': 'line', 'name': 'Estado de alarma', 'line': {'color': 'rgb(100, 105, 109)', 'width': '4', 'dash': 'dot'}},
            {'x': [datetime.strptime('2020-03-29 00:00', '%Y-%m-%d %H:%M'), datetime.strptime('2020-03-29 00:01', '%Y-%m-%d %H:%M')], 'y': [
                0, dataset.df[dataset.df['CCAA'] == comunidad]['Casos'].max()], 'type': 'line', 'name': 'Confinamiento estricto', 'line': {'color': 'rgb(143, 147, 150)', 'width': '4', 'dash': 'dot'}},
            {'x': [datetime.strptime('2020-04-13 00:00', '%Y-%m-%d %H:%M'), datetime.strptime('2020-04-13 00:01', '%Y-%m-%d %H:%M')], 'y': [
                0, dataset.df[dataset.df['CCAA'] == comunidad]['Casos'].max()], 'type': 'line', 'name': 'Vuelta al trabajo', 'line': {'color': 'rgb(100, 105, 109) ', 'width': '4', 'dash': 'dot'}}
        ],
        'layout': go.Layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation='h', y=1.2),
            margin=dict(
                l=0,
                r=20,
                b=25,
                t=0),
            xaxis={
                'showgrid': False,
                'autorange': True,
                'zeroline': False,
                'showline': False,


            },
            yaxis={
                'showgrid': False,
                'autorange': True,
                'zeroline': False,
                'showline': False,
                'showticklabels': False,
                'range': [0, dataset.df[dataset.df['CCAA'] == comunidad]['Casos'].max() + 20]

            }
        )
    }


@app.callback(
    Output('daily-increment', 'figure'), [Input('comunidad-drop', 'value')]
)
def update_daily_increment(comunidad):
    df = dataset.df[dataset.df['CCAA'] == comunidad]
    data = []
    cols = ['Casos', 'Fallecidos', 'Recuperados']

    for col in cols:
        data.append(
            {
                'x': pd.DatetimeIndex(df['Fecha']).to_pydatetime(),
                'y': df[col].diff(),
                'name': col,
                'type': 'bar',
                'text': df[col].diff(),
                'textposition': 'auto'
            }
        )

    return {
        'data': data,
        'layout': go.Layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation='h', y=1.2),
            barmode='stack',
            margin=dict(
                l=0,
                r=20,
                b=25,
                t=0),
            xaxis={
                'showgrid': False,
                'autorange': True,
                'zeroline': False,
                'showline': False,


            },
            yaxis={
                'showgrid': False,
                'autorange': True,
                'zeroline': False,
                'showline': False,
                'showticklabels': False,
                'range': [0, df['Casos'].diff().max() + 10]
            }
        )
    }


@app.callback(
    Output('val_Infectados', 'children'),  [Input('comunidad-drop', 'value')]
)
def value_infectados(comunidad):
    return "{0:,g}".format(dataset.df[dataset.df['CCAA'] == comunidad]['Casos'].iloc[-1]).replace(",", ".")


@app.callback(
    Output('val_Fallecidos', 'children'),  [Input('comunidad-drop', 'value')]
)
def value_fallecidos(comunidad):
    return "{0:,g}".format(dataset.df[dataset.df['CCAA'] == comunidad]['Fallecidos'].iloc[-1]).replace(",", ".")


@app.callback(
    Output('val_Recuperados', 'children'),  [Input('comunidad-drop', 'value')]
)
def value_recuperados(comunidad):
    return "{0:,g}".format(dataset.df[dataset.df['CCAA'] == comunidad]['Recuperados'].iloc[-1]).replace(",", ".")


@app.callback(
    Output('val_Casos activos', 'children'),  [
        Input('comunidad-drop', 'value')]
)
def value_activos(comunidad):
    casos = dataset.df[dataset.df['CCAA'] == comunidad]['Casos'].iloc[-1]
    fallecidos = dataset.df[dataset.df['CCAA']
                            == comunidad]['Fallecidos'].iloc[-1]
    recuperados = dataset.df[dataset.df['CCAA']
                             == comunidad]['Recuperados'].iloc[-1]

    return "{0:,g}".format(casos - fallecidos - recuperados).replace(",", ".")


@app.callback(
    Output('inc_Infectados', 'children'),  [Input('comunidad-drop', 'value')]
)
def inc_infectados(comunidad):
    return "🠝 {0:,g} (24h)".format(dataset.df[dataset.df['CCAA'] == comunidad]['Casos'].iloc[-1] - dataset.df[dataset.df['CCAA'] == comunidad]['Casos'].iloc[-2]).replace(',', '.')


@app.callback(
    Output('inc_Fallecidos', 'children'),  [Input('comunidad-drop', 'value')]
)
def inc_fallecidos(comunidad):
    return "🠝 {0:,g} (24h)".format(dataset.df[dataset.df['CCAA'] == comunidad]['Fallecidos'].iloc[-1] - dataset.df[dataset.df['CCAA'] == comunidad]['Fallecidos'].iloc[-2]).replace(',', '.')


@app.callback(
    Output('inc_Recuperados', 'children'),  [Input('comunidad-drop', 'value')]
)
def inc_recuperados(comunidad):
    return "🠝 {0:,g} (24h)".format(dataset.df[dataset.df['CCAA'] == comunidad]['Recuperados'].iloc[-1] - dataset.df[dataset.df['CCAA'] == comunidad]['Recuperados'].iloc[-2]).replace(',', '.')
