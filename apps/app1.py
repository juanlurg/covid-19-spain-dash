# -*- coding: utf-8 -*-
import json
from datetime import datetime

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State

from app import app
from apps import common
from apps.data import dataset

colors_dict = {
    "Casos activos": 'primary',
    "Infectados": 'danger',
    "Fallecidos": 'secondary',
    "Recuperados": 'success'
}


with open('geo.json') as response:
    communities = json.load(response)


cards_content = []

for i, (metric, value) in enumerate(dataset.metrics_dict.items()):
    cards_content.append(
        dbc.Card(
            dbc.CardBody(
                [html.H6([metric],
                         className="card-subtitle", style={'marginBottom': '5px'}),
                    html.H4("{:n}".format(
                        value), className="card-title"),
                    html.H6(["🠝", dataset.inc_dict[metric], " (24h.)"],
                            className="card-subtitle"),




                 ]
            ),

            color=colors_dict[metric],
            inverse=True,
            style={'marginTop': "15px", "width": "190px"}
        )
    )

cards_content.append(
    dbc.Card([
        dbc.CardHeader("Ver en el mapa: "),
        dbc.CardBody(
            [
                dcc.Dropdown(
                    id='dimension-mapa',
                    options=[
                        {'label': 'Casos activos', 'value': 'Casos Activos'},
                        {'label': 'Infectados', 'value': 'Casos'},
                        {'label': 'Fallecidos', 'value': 'Fallecidos'},
                        {'label': 'Recuperados', 'value': 'Recuperados'}
                    ],
                    placeholder="Visualizar en el mapa",

                    clearable=False,
                    value='Casos Activos',
                    searchable=False
                )
            ]
        )],
        style={'marginTop': "15px", "width": "190px"},
    )
)


fig = [go.Choroplethmapbox(geojson=communities, locations=dataset.hoy['cod_ine'], z=dataset.hoy['Casos Activos'],
                           featureidkey='properties.codigo',
                           colorscale="Blues", zmin=dataset.hoy['Casos Activos'].min(), zmax=dataset.hoy['Casos Activos'].max(),
                           marker_opacity=1, marker_line_width=0, showlegend=False, showscale=False
                           )
       ]


layout = go.Layout(mapbox_style="carto-positron",
                   mapbox_zoom=5, mapbox_center={"lat": 40.416775, "lon": -3.703790}, autosize=False,
                   width=1000,
                   height=700,
                   margin=dict(
                       l=0,
                       r=0,
                       b=0,
                       t=0))


page = dbc.Container(
    [
        common.navbar,
        dbc.Row([
            dbc.Col(cards_content, width=2, style={'position': 'fixed'}),
            dbc.Col(dcc.Graph(id='mapa-spain',
                              figure={"data": fig, "layout": layout}, responsive=True), width=10, style={'marginLeft': '260px'})
        ],
            style={"paddingLeft": "10px", 'height': 'calc(100vh - 55px)'
                   }
        ),

        dbc.Row([
            dbc.Col([html.H1("Evolución diaria", className="display-5", style={'paddingTop': '15px'}),
                     html.P(
                "Gráfico histórico temporal de contagios, fallecidos y recuperados con fechas clave destacadas.",
                className="lead",
            ),
                html.Hr(className="my-2"),
                dcc.Graph(figure={
                    'data': [
                        {'x': dataset.df_spain.index.to_pydatetime(),
                         'y': dataset.df_spain['Casos'], 'type': 'scatter', 'name': 'Casos'},
                        {'x': dataset.df_spain.index.to_pydatetime(),
                         'y': dataset.df_spain['Fallecidos'], 'type': 'scatter', 'name': 'Fallecidos'},
                        {'x': dataset.df_spain.index.to_pydatetime(),
                         'y': dataset.df_spain['Recuperados'], 'type': 'scatter', 'name': 'Recuperados'},
                        {'x': [datetime.strptime('2020-03-14 00:00', '%Y-%m-%d %H:%M'), datetime.strptime('2020-03-14 00:01', '%Y-%m-%d %H:%M')], 'y': [
                            0, dataset.df_spain['Casos'].max()], 'type': 'line', 'name': 'Estado de alarma'},
                        {'x': [datetime.strptime('2020-03-29 00:00', '%Y-%m-%d %H:%M'), datetime.strptime('2020-03-29 00:01', '%Y-%m-%d %H:%M')], 'y': [
                            0, dataset.df_spain['Casos'].max()], 'type': 'line', 'name': 'Confinamiento estricto'}
                    ],
                    'layout': go.Layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        legend=dict(orientation='h', y=1.2)
                    )
                }
            )], width={"size": 10, "offset": 2})
        ],
            style={"paddingLeft": "10px", 'height': 'calc(100vh - 55px)'}
        )


    ],
    fluid=True,
    style={'padding': '0px', 'backgroundColor': '#d4dadc'}
)


@app.callback(Output('mapa-spain', 'figure'), [Input('dimension-mapa', 'value')])
def update_mapa(selected_dimension):

    color_scale_dict = {
        "Casos Activos": 'Blues',
        "Casos": 'OrRd',
        "Fallecidos": 'Greys',
        "Recuperados": 'Greens'
    }
    fig = [go.Choroplethmapbox(geojson=communities, locations=dataset.hoy['cod_ine'], z=dataset.hoy[selected_dimension],
                               featureidkey='properties.codigo',
                               colorscale=color_scale_dict[selected_dimension], zmin=dataset.hoy[selected_dimension].min(), zmax=dataset.hoy[selected_dimension].max(),
                               marker_opacity=1, marker_line_width=0, showlegend=False, showscale=False
                               )
           ]

    layout = go.Layout(
        mapbox_style="carto-positron",
        mapbox_zoom=5, mapbox_center={"lat": 40.416775, "lon": -3.703790}, autosize=False,
        width=1200,
        height=650,
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0))

    return {'data': fig, 'layout': layout}


@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open
