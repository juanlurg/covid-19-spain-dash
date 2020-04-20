# -*- coding: utf-8 -*-
from datetime import datetime

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State

from app import app
from apps import common
from apps.data import dataset

page = dbc.Container(
    [
        common.navbar,
        dbc.Row([
            dbc.Col([
                html.H3("Incremento de Casos", className="display-6",
                        style={'position': 'absolute', 'marginTop': '15px', 'zIndex': '1'}),

                # Daily new cases chart
                dcc.Graph(
                    id='inc_casos_chart',
                    figure={
                        'data': [
                            {'x': [datetime.strptime('2020-03-14 00:00', '%Y-%m-%d %H:%M'), datetime.strptime('2020-03-14 00:01', '%Y-%m-%d %H:%M')], 'y': [
                                0,  dataset.df_spain['inc_Casos'].max()], 'type': 'line', 'name': 'Estado de alarma', 'line': {'color': 'rgb(100, 105, 109)', 'width': '4', 'dash': 'dot'}},
                            {'x': [datetime.strptime('2020-03-29 00:00', '%Y-%m-%d %H:%M'), datetime.strptime('2020-03-29 00:01', '%Y-%m-%d %H:%M')], 'y': [
                                0,  dataset.df_spain['inc_Casos'].max()], 'type': 'line', 'name': 'Confinamiento estricto', 'line': {'color': 'rgb(143, 147, 150)', 'width': '4', 'dash': 'dot'}},
                            {'x': [datetime.strptime('2020-04-13 00:00', '%Y-%m-%d %H:%M'), datetime.strptime('2020-04-13 00:01', '%Y-%m-%d %H:%M')], 'y': [
                                0,  dataset.df_spain['inc_Casos'].max()], 'type': 'line', 'name': 'Vuelta al trabajo', 'line': {'color': 'rgb(100, 105, 109)', 'width': '4', 'dash': 'dot'}},
                            {
                                'x': dataset.df_spain.index.to_pydatetime(), 'y': dataset.df_spain['inc_Casos'], 'type': 'bar', 'name': 'Casos', 'text': dataset.df_spain['inc_Casos'],
                                'textposition': 'auto', 'marker': {'color': 'rgb(39, 128, 227)'}
                            }
                        ],
                        'layout': go.Layout(
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            legend=dict(orientation='h', y=0.85),
                            margin=dict(
                                l=0,
                                r=0,
                                b=15,
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
                                'showticklabels': False
                            }
                        )
                    }, style={'marginTop': '15px', 'height': '250px'}
                )
            ], width=10),

            # Cards with last 7 days and last 24h summary metric
            dbc.Col([dbc.Card(
                dbc.CardBody(
                    [html.H6(["Últimos 7 días"],
                             className="card-subtitle", style={'marginBottom': '5px'}),
                     html.H4("🠝 {:.2%}".format(
                         dataset.df_spain['inc_pct_Casos'].iloc[-6: -1].mean()), className="card-title")]
                ),
                color='info',
                inverse=True,
                style={'marginTop': "15px", "width": "190px"}
            ),
                dbc.Card(
                dbc.CardBody(
                    [html.H6(["Últimas 24 horas"],
                             className="card-subtitle", style={'marginBottom': '5px'}),
                     html.H4("🠝 {:.2%}".format(
                         dataset.df_spain['inc_pct_Casos'].iloc[-1]), className="card-title")]
                ),
                outline=True,
                color='info',
                style={'marginTop': "15px", "width": "190px"}
            )], width=2, align='center')
        ], style={'paddingLeft': '30px', 'paddingRight': '0px', 'paddingBottom': '20px'}
        ),
        dbc.Row([
            dbc.Col([
                html.H3("Incremento de Fallecidos", className="display-6",
                        style={'position': 'absolute', 'marginTop': '15px', 'zIndex': '1'}),

                # Daily new deceased chart
                dcc.Graph(
                    id='inc_casos_chart',
                    figure={
                        'data': [
                            {'x': [datetime.strptime('2020-03-14 00:00', '%Y-%m-%d %H:%M'), datetime.strptime('2020-03-14 00:01', '%Y-%m-%d %H:%M')], 'y': [
                                0,  dataset.df_spain['inc_Fallecidos'].max()], 'type': 'line', 'name': 'Estado de alarma', 'line': {'color': 'rgb(100, 105, 109)', 'width': '4', 'dash': 'dot'}},
                            {'x': [datetime.strptime('2020-03-29 00:00', '%Y-%m-%d %H:%M'), datetime.strptime('2020-03-29 00:01', '%Y-%m-%d %H:%M')], 'y': [
                                0,  dataset.df_spain['inc_Fallecidos'].max()], 'type': 'line', 'name': 'Confinamiento estricto', 'line': {'color': 'rgb(143, 147, 150)', 'width': '4', 'dash': 'dot'}},
                            {'x': [datetime.strptime('2020-04-13 00:00', '%Y-%m-%d %H:%M'), datetime.strptime('2020-04-13 00:01', '%Y-%m-%d %H:%M')], 'y': [
                                0,  dataset.df_spain['inc_Fallecidos'].max()], 'type': 'line', 'name': 'Vuelta al trabajo', 'line': {'color': 'rgb(100, 105, 109)', 'width': '4', 'dash': 'dot'}},
                            {
                                'x': dataset.df_spain.index, 'y': dataset.df_spain['inc_Fallecidos'], 'type': 'bar', 'name': 'Fallecidos', 'text': dataset.df_spain['inc_Fallecidos'], 'textposition': 'auto', 'marker': {'color': 'rgb(55, 58, 60)'}
                            }
                        ],
                        'layout': go.Layout(
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            legend=dict(orientation='h', y=0.85),
                            margin=dict(
                                l=0,
                                r=0,
                                b=15,
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
                                'showticklabels': False
                            }
                        )
                    }, style={'marginTop': '15px', 'height': '250px'}
                )
            ], width=10),

            # Cards with last 7 days and last 24h metrics
            dbc.Col([dbc.Card(
                dbc.CardBody(
                    [html.H6(["Últimos 7 días"],
                             className="card-subtitle", style={'marginBottom': '5px'}),
                     html.H4("🠝 {:.2%}".format(
                         dataset.df_spain['inc_pct_Fallecidos'].iloc[-6: -1].mean()), className="card-title")
                     ]
                ),

                color='primary',
                inverse=True,
                style={'marginTop': "15px", "width": "190px"}
            ),
                dbc.Card(
                dbc.CardBody(
                    [html.H6(["Últimas 24 horas"],
                             className="card-subtitle", style={'marginBottom': '5px'}),
                     html.H4("🠝 {:.2%}".format(
                         dataset.df_spain['inc_pct_Fallecidos'].iloc[-1]), className="card-title")
                     ]
                ),
                outline=True,
                color='primary',

                style={'marginTop': "15px", "width": "190px"}
            )], width=2, align='center')
        ], style={'paddingLeft': '30px', 'paddingRight': '0px', 'paddingBottom': '20px'}
        ),
        dbc.Row([
            dbc.Col([
                html.H3("Incremento de Recuperados", className="display-6",
                        style={'position': 'absolute', 'marginTop': '15px', 'zIndex': '1'}),

                # Daily new recovered chart
                dcc.Graph(
                    id='inc_casos_chart',
                    figure={
                        'data': [
                            {'x': [datetime.strptime('2020-03-14 00:00', '%Y-%m-%d %H:%M'), datetime.strptime('2020-03-14 00:01', '%Y-%m-%d %H:%M')], 'y': [
                                0,  dataset.df_spain['inc_Recuperados'].max()], 'type': 'line', 'name': 'Estado de alarma', 'line': {'color': 'rgb(100, 105, 109)', 'width': '4', 'dash': 'dot'}},
                            {'x': [datetime.strptime('2020-03-29 00:00', '%Y-%m-%d %H:%M'), datetime.strptime('2020-03-29 00:01', '%Y-%m-%d %H:%M')], 'y': [
                                0,  dataset.df_spain['inc_Recuperados'].max()], 'type': 'line', 'name': 'Confinamiento estricto', 'line': {'color': 'rgb(143, 147, 150)', 'width': '4', 'dash': 'dot'}},
                            {'x': [datetime.strptime('2020-04-13 00:00', '%Y-%m-%d %H:%M'), datetime.strptime('2020-04-13 00:01', '%Y-%m-%d %H:%M')], 'y': [
                                0,  dataset.df_spain['inc_Recuperados'].max()], 'type': 'line', 'name': 'Vuelta al trabajo', 'line': {'color': 'rgb(100, 105, 109)', 'width': '4', 'dash': 'dot'}},

                            {
                                'x': dataset.df_spain.index, 'y': dataset.df_spain['inc_Recuperados'], 'type': 'bar', 'name': 'Recuperados', 'text': dataset.df_spain['inc_Recuperados'], 'textposition': 'auto', 'marker': {'color': 'rgb(63, 182, 24)'}
                            }
                        ],
                        'layout': go.Layout(
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            legend=dict(orientation='h', y=0.85),
                            margin=dict(
                                l=0,
                                r=0,
                                b=15,
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
                                'showticklabels': False
                            }
                        )
                    }, style={'marginTop': '15px', 'height': '250px'}
                )
            ], width=10),

            # Cards with las 7 days and las 24h metric
            dbc.Col([dbc.Card(
                dbc.CardBody(
                    [html.H6(["Últimos 7 días"],
                             className="card-subtitle", style={'marginBottom': '5px'}),
                     html.H4("🠝 {:.2%}".format(
                         dataset.df_spain['inc_pct_Recuperados'].iloc[-6: -1].mean()), className="card-title")
                     ]
                ),
                color='success',
                inverse=True,
                style={'marginTop': "15px", "width": "190px"}
            ),
                dbc.Card(
                dbc.CardBody(
                    [html.H6(["Últimas 24 horas"],
                             className="card-subtitle", style={'marginBottom': '5px'}),
                     html.H4("🠝 {:.2%}".format(
                         dataset.df_spain['inc_pct_Recuperados'].iloc[-1]), className="card-title")
                     ]
                ),
                outline=True,
                color='success',
                style={'marginTop': "15px", "width": "190px"}
            )], width=2, align='center')
        ], style={'paddingLeft': '30px', 'paddingRight': '0px'}
        ),
    ],
    fluid=True,
    style={'padding': '0px', 'backgroundColor': '#d4dadc'}
)
