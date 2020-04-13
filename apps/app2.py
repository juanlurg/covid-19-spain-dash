# -*- coding: utf-8 -*-

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State

from apps import common
from apps.data import dataset

page = dbc.Container(
    [
        common.navbar,
        html.H5("En desarrollo"),
        dbc.Row([
            dbc.Col(
                dcc.Graph(figure={
                    'data': [
                        {'x': dataset.df_spain.index,
                         'y': dataset.df_spain['Casos'], 'type': 'scatter', 'name': 'Casos'},
                        {'x': dataset.df_spain.index,
                         'y': dataset.df_spain['Fallecidos'], 'type': 'scatter', 'name': 'Fallecidos'},
                        {'x': dataset.df_spain.index,
                         'y': dataset.df_spain['Recuperados'], 'type': 'scatter', 'name': 'Recuperados'}
                    ],
                    'layout': go.Layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)'
                    )
                }
                ), width=12)
        ],
            style={"paddingLeft": "10px"}
        )


    ],
    fluid=True,
    style={'padding': '0px', 'backgroundColor': '#d4dadc'}
)
