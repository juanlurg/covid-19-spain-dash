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


page = dbc.Container(
    [
        navbar,

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

