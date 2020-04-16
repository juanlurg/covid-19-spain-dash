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


cards_content = []
cards_mobile = []

for i, (metric, value) in enumerate(dataset.metrics_dict.items()):
    cards_content.append(
        dbc.Card(
            dbc.CardBody(
                [html.H6([metric],
                         className="card-subtitle", style={'marginBottom': '5px'}),
                    html.H4("{:,}".format(
                        value).replace(",", "."), className="card-title"),  # Heroku only allows EN-us locale in apps so workaround to format numbers following spanish way
                    html.H6(["🠝 {0:,g} (24h.)".format(dataset.inc_dict[metric]).replace(',', '.')],
                            className="card-subtitle"),




                 ]
            ),

            color=colors_dict[metric],
            inverse=True,
            style={'marginTop': "15px"}
        )
    )
    cards_mobile.append(
        dbc.Card(
            dbc.CardBody(
                [html.H6([metric],
                         className="card-subtitle", style={'marginBottom': '5px', 'fontSize': '60px'}),
                    html.H4("{:,}".format(
                        value).replace(",", "."), className="card-title", style={'fontSize': '140px'}),  # Heroku only allows EN-us locale in apps so workaround to format numbers following spanish way
                    html.H6(["🠝 {0:,g} (24h.)".format(dataset.inc_dict[metric]).replace(',', '.')],
                            className="card-subtitle", style={'fontSize': '60px'}),




                 ],
                style={'padding': '45px'}
            ),

            color=colors_dict[metric],
            inverse=True,
            style={'marginTop': "15px", 'height': "20vh"}
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
            dbc.Col(cards_content, width=2, style={
                    'position': 'fixed'}, className='hide-mobile h-100', md=12, lg=2),
            dbc.Col([
                html.H1(["Vista de mapa", dcc.Dropdown(
                    id='dimension-mapa',
                    options=[
                        {'label': 'Casos activos', 'value': 'Casos Activos'},
                        {'label': 'Infectados', 'value': 'Casos'},
                        {'label': 'Fallecidos', 'value': 'Fallecidos'},
                        {'label': 'Recuperados', 'value': 'Recuperados'},
                        {'label': 'Activos/1M poblacion',
                            'value': 'casos_activos_1k'},
                        {'label': 'Casos/1M poblacion', 'value': 'casos_1k'},

                        {'label': 'Fallecidos/1M poblacion',
                            'value': 'fallecidos_1k'},
                        {'label': 'Recuperados/1M poblacion',
                            'value': 'recuperados_1k'},
                    ],
                    placeholder="Visualizar en el mapa",

                    clearable=False,
                    value='Casos Activos',
                    searchable=False,
                    style={'fontSize': '18.75px', 'marginTop': '8px'}
                )], className="display-5",
                    style={'position': 'absolute', 'marginTop': '15px', 'zIndex': '1', 'width': '280px'}),

                dcc.Graph(id='mapa-spain',
                          figure={"data": fig, "layout": layout}, responsive=True)], width={'size': 10, 'offset': 2}, className='d-sm-none d-lg-block', style={'height': 'calc(100vh - 55px)'
                                                                                                                                                               })
        ],
            style={"paddingLeft": "10px", 'height': 'calc(100vh - 55px)'
                   },
            className='d-sm-none d-lg-block'
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
                         'y': dataset.df_spain['Casos'], 'type': 'scatter', 'name': 'Casos',  'marker': {'color': 'rgb(39, 128, 227)'}},
                        {'x': dataset.df_spain.index.to_pydatetime(),
                         'y': dataset.df_spain['Fallecidos'], 'type': 'scatter', 'name': 'Fallecidos', 'marker': {'color': 'rgb(55, 58, 60)'}},
                        {'x': dataset.df_spain.index.to_pydatetime(),
                         'y': dataset.df_spain['Recuperados'], 'type': 'scatter', 'name': 'Recuperados', 'marker': {'color': 'rgb(63, 182, 24)'}},
                        {'x': [datetime.strptime('2020-03-14 00:00', '%Y-%m-%d %H:%M'), datetime.strptime('2020-03-14 00:01', '%Y-%m-%d %H:%M')], 'y': [
                            0, dataset.df_spain['Casos'].max()], 'type': 'line', 'name': 'Estado de alarma', 'line': {'color': 'rgb(100, 105, 109)', 'width': '4', 'dash': 'dot'}},
                        {'x': [datetime.strptime('2020-03-29 00:00', '%Y-%m-%d %H:%M'), datetime.strptime('2020-03-29 00:01', '%Y-%m-%d %H:%M')], 'y': [
                            0, dataset.df_spain['Casos'].max()], 'type': 'line', 'name': 'Confinamiento estricto', 'line': {'color': 'rgb(143, 147, 150)', 'width': '4', 'dash': 'dot'}}
                    ],
                    'layout': go.Layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        legend=dict(orientation='h', y=1.2)
                    )
                }
            )], lg={"size": 10, "offset": 2}, md={"size": 12, "offset": 0})
        ],
            style={"paddingLeft": "10px", 'height': '560px'},
            className="d-sm-none d-lg-block"
        ),

        dbc.Row([
            dbc.Col([html.H1("Evolución por comunidades", className="display-5", style={'paddingTop': '15px'}),
                     html.P(
                "Gráfico acumulado de casos por comunidad autónoma.",
                className="lead",
            ),
                html.Hr(className="my-2"),
                dcc.Graph(figure={
                    'data': dataset.data,
                    'layout': go.Layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        legend=dict(orientation='h', y=1.2),
                        barmode='stack'
                    )
                }
            )], width={"size": 10, "offset": 2})
        ],
            style={"paddingLeft": "10px", 'height': '560px'},
            className="d-sm-none d-lg-block"
        ),
        dbc.Row([
            dbc.Col(cards_mobile, width=2,
                    className='hide-mobile h-100', md=12, lg=2),

        ],
            style={"paddingLeft": "10px", 'height': 'calc(100vh - 55px)'
                   },
            className="d-sm-block d-lg-none"
        ),
        dbc.Row([
            dbc.Col([html.H1("Evolución diaria", className="display-5", style={'paddingTop': '15px', 'fontSize': '70px'}),

                     dcc.Graph(figure={
                         'data': [
                             {'x': dataset.df_spain.index.to_pydatetime(),
                              'y': dataset.df_spain['Casos'], 'type': 'scatter', 'name': 'Casos',  'marker': {'color': 'rgb(39, 128, 227)'}},
                             {'x': dataset.df_spain.index.to_pydatetime(),
                              'y': dataset.df_spain['Fallecidos'], 'type': 'scatter', 'name': 'Fallecidos', 'marker': {'color': 'rgb(55, 58, 60)'}},
                             {'x': dataset.df_spain.index.to_pydatetime(),
                              'y': dataset.df_spain['Recuperados'], 'type': 'scatter', 'name': 'Recuperados', 'marker': {'color': 'rgb(63, 182, 24)'}},
                             {'x': [datetime.strptime('2020-03-14 00:00', '%Y-%m-%d %H:%M'), datetime.strptime('2020-03-14 00:01', '%Y-%m-%d %H:%M')], 'y': [
                                 0, dataset.df_spain['Casos'].max()], 'type': 'line', 'name': 'Estado de alarma', 'line': {'color': 'rgb(100, 105, 109)', 'width': '4', 'dash': 'dot'}},
                             {'x': [datetime.strptime('2020-03-29 00:00', '%Y-%m-%d %H:%M'), datetime.strptime('2020-03-29 00:01', '%Y-%m-%d %H:%M')], 'y': [
                                 0, dataset.df_spain['Casos'].max()], 'type': 'line', 'name': 'Confinamiento estricto', 'line': {'color': 'rgb(143, 147, 150)', 'width': '4', 'dash': 'dot'}}
                         ],
                         'layout': go.Layout(
                             paper_bgcolor='rgba(0,0,0,0)',
                             plot_bgcolor='rgba(0,0,0,0)',
                             legend=dict(orientation='h', y=1.2)
                         ),

                     }, responsive=True,
                style={'height': '42%'}
            ),
                html.H1("Evolución por comunidades",
                        className="display-5", style={'paddingTop': '15px', 'fontSize': '70px'}),
                dcc.Graph(figure={
                    'data': dataset.data,
                    'layout': go.Layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        legend=dict(orientation='h', y=1.2),
                        barmode='stack'
                    )
                },
                style={'height': '42%'}
            )
            ], lg={"size": 10, "offset": 2}, md={"size": 12, "offset": 0}, className='h-100')
        ],
            style={"paddingLeft": "10px", 'height': 'calc(100vh - 55px)'},
            className="d-sm-block d-lg-none d-lg-none d-lg-none"
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
        "Recuperados": 'Greens',
        "casos_activos_1k": 'Blues',
        "casos_1k": 'OrRd',
        "fallecidos_1k": 'Greys',
        "recuperados_1k": 'Greens',
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
