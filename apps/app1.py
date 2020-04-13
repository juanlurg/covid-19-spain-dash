# -*- coding: utf-8 -*-
import os
import json
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_bootstrap_components as dbc
import numpy as np
import locale
import plotly.express as px
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go

from app import app


file_data = 'https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/ccaa_covid19_datos_isciii.csv'

df = pd.read_csv(file_data)

df['Fecha'] = pd.to_datetime(df['Fecha'])
last_update = df['Fecha'].max()
last_update_str = last_update.strftime('%d/%m/%Y')
df_grouped = df.groupby('Fecha').sum()
infected = df_grouped['Casos'].iloc[-1].astype(np.int64)
deseased = df_grouped['Fallecidos'].iloc[-1].astype(np.int64)
recovered = df_grouped['Recuperados'].iloc[-1].astype(np.int64)
active_cases = infected - deseased - recovered

inc_infected = infected - df_grouped['Casos'].iloc[-2]
inc_deseased = deseased - df_grouped['Fallecidos'].iloc[-2]
inc_recovered = recovered - df_grouped['Recuperados'].iloc[-2]

hoy = df[df['Fecha'] == last_update]
hoy['Casos Activos'] = hoy['Casos'] - hoy['Fallecidos'] - hoy['Recuperados']
hoy = hoy.drop(columns=['Hospitalizados', 'UCI'])


df_spain = df.groupby('Fecha').sum()
df_spain = df_spain.drop(columns=['cod_ine'])


with open('geo.json') as response:
    communities = json.load(response)

inc_dict = {
    "Casos activos": inc_infected,
    "Infectados": inc_infected,
    "Fallecidos": inc_deseased,
    "Recuperados": inc_recovered
}


metrics_dict = {
    "Casos activos": active_cases,
    "Infectados": infected,
    "Fallecidos": deseased,
    "Recuperados": recovered
}

colors_dict = {
    "Casos activos": 'primary',
    "Infectados": 'danger',
    "Fallecidos": 'secondary',
    "Recuperados": 'success'
}

navbar = dbc.NavbarSimple(
    children=[

        dbc.NavItem(dbc.NavLink("Incrementos diarios", href="incrementos")),
        dbc.NavItem(dbc.NavLink("Detalle comunidad", href='#')),
        dbc.NavItem(dbc.NavLink("Modelos matemáticos", href='#')),
        dbc.NavItem(
            dbc.NavLink(html.I(className="fas fa-question-circle",
                               id="open"), href="#"),
        ),
        dbc.Modal(
            [
                dbc.ModalHeader("Sobre este proyecto"),
                dbc.ModalBody(dcc.Markdown('''
                 Realizado por [**Juan Luis Ramirez**](https://github.com/juanlurg)
                 
                 Para el desarrollo del proyecto se han usado los datos publicados por [Datadista](https://github.com/datadista/datasets/tree/master/COVID%2019) y el GeoJSON de las comunidades autónomas de [Albert del Amor](https://albertdelamor.carto.com/tables/comunidades_autonomas_etrs89_30n/public/map).

                 El código desarrollado para este proyecto, así como otros Jupyter Notebooks usados para analizar el estado de los datos de la pandemia en España están disponibles en [el repositorio del proyecto](https://github.com/juanlurg/covid-19-spain-dash), en la web podrá encontrar artículos explicando paso a paso el desarrollo.


                 Contacto: [**juanlu.rgarcia@gmail.com**](mailto:juanlu.rgarcia@gmail.com)
                ''')),
                dbc.ModalFooter(
                    dbc.Button("Cerrar", id="close", className="ml-auto")
                ),
            ],
            id="modal",
            centered=True
        ),

    ],
    brand="COVID-19 en España (act. {})".format(last_update_str),
    brand_href="#",
    color="primary",
    dark=True,
    fluid=True
)


cards_content = [
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



]

for metric in metrics_dict:
    cards_content.append(
        dbc.Card(
            dbc.CardBody(
                [html.H6([metric],
                         className="card-subtitle", style={'marginBottom': '5px'}),
                    html.H4("{:n}".format(
                        metrics_dict[metric]), className="card-title"),
                    html.H6(["🠝", inc_dict[metric], " (24h.)"],
                            className="card-subtitle"),




                 ]
            ),

            color=colors_dict[metric],
            inverse=True,
            style={'marginTop': "15px", "width": "190px"}
        )
    )


fig = [go.Choroplethmapbox(geojson=communities, locations=hoy['cod_ine'], z=hoy['Casos Activos'],
                           featureidkey='properties.codigo',
                           colorscale="Blues", zmin=hoy['Casos Activos'].min(), zmax=hoy['Casos Activos'].max(),
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
        navbar,
        dbc.Row([
            dbc.Col(cards_content, width=2),
            dbc.Col(dcc.Graph(id='mapa-spain',
                              figure={"data": fig, "layout": layout}), width=10)
        ],
            style={"paddingLeft": "10px"}
        ),
        dbc.Row([
            dbc.Col(
                dcc.Graph(figure={
                    'data': [
                        {'x': df_spain.index,
                         'y': df_spain['Casos'], 'type': 'scatter', 'name': 'Casos'},
                        {'x': df_spain.index,
                         'y': df_spain['Fallecidos'], 'type': 'scatter', 'name': 'Fallecidos'},
                        {'x': df_spain.index,
                         'y': df_spain['Recuperados'], 'type': 'scatter', 'name': 'Recuperados'}
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


@app.callback(Output('mapa-spain', 'figure'), [Input('dimension-mapa', 'value')])
def update_mapa(selected_dimension):

    color_scale_dict = {
        "Casos Activos": 'Blues',
        "Casos": 'OrRd',
        "Fallecidos": 'Greys',
        "Recuperados": 'Greens'
    }
    fig = [go.Choroplethmapbox(geojson=communities, locations=hoy['cod_ine'], z=hoy[selected_dimension],
                               featureidkey='properties.codigo',
                               colorscale=color_scale_dict[selected_dimension], zmin=hoy[selected_dimension].min(), zmax=hoy[selected_dimension].max(),
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
