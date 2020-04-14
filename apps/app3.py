# -*- coding: utf-8 -*-

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
        dbc.Row(
            dbc.Col(dbc.Alert(
                [
                    html.H4("¡Casi!", className="alert-heading"),
                    html.P(
                        "Este contenido aún no está disponible, si deseas colaborar pincha en el icono de la interrogación de arriba ;) "

                    ),
                    html.Hr(),
                    html.P(
                        "Muchas gracias",
                        className="mb-0",
                    ),
                ]
            ), width={"size": 6, "offset": 3}, style={'marginTop': '15px'})
        )





    ],
    fluid=True,
    style={'padding': '0px', 'backgroundColor': '#d4dadc'}
)
