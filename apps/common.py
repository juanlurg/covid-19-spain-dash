import json
import locale
import os

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State

from apps.data import dataset

navbar = dbc.NavbarSimple(
    children=[

        dbc.NavItem(dbc.NavLink("📈 Incrementos diarios",
                                id='tooltip-inc', href="incrementos")),
        dbc.NavItem(dbc.NavLink("🏠 Detalle comunidad",
                                id='tooltip-comunidad', href='comunidad')),
        dbc.NavItem(dbc.NavLink("🧾 Modelos matemáticos",
                                id='tooltip-modelos', href='modelos')),
        dbc.NavItem(
            dbc.NavLink("🧔",
                        id="open", href="#"), id='sobremi'
        ),
        dbc.Modal(
            [
                dbc.ModalHeader("Sobre este proyecto"),
                dbc.ModalBody(dcc.Markdown('''
                 Para el desarrollo del proyecto se han usado los datos publicados por [Datadista](https://github.com/datadista/datasets/tree/master/COVID%2019) y el GeoJSON de las comunidades autónomas de [Albert del Amor](https://albertdelamor.carto.com/tables/comunidades_autonomas_etrs89_30n/public/map).

                 El código desarrollado para este proyecto, así como otros Jupyter Notebooks usados para analizar el estado de los datos de la pandemia en España están disponibles en [el repositorio del proyecto](https://github.com/juanlurg/covid-19-spain-dash), en la web podrá encontrar artículos explicando paso a paso el desarrollo. Principalmente para este proyecto se ha usado Python con Dash, plotly y pandas.

                 Realizado por [**Juan Luis Ramirez**](https://github.com/juanlurg)
                 
                 Contacto: [**juanlu.rgarcia@gmail.com**](mailto:juanlu.rgarcia@gmail.com)
                ''')),
                dbc.ModalFooter(
                    dbc.Button("Cerrar", id="close", className="ml-auto")
                ),
            ],
            id="modal",
            centered=True
        ),
        dbc.Tooltip(
            "Visualice los incrementos diarios de contagios, fallecidos y recuperados",
            target="tooltip-inc",
        ),
        dbc.Tooltip(
            "Vista concreta del estado de cada comunidad",
            target="tooltip-comunidad",
        ),
        dbc.Tooltip(
            "Usando modelos matemáticos para predecir la evolución de la pandemia",
            target="tooltip-modelos",
        ),
        dbc.Tooltip(
            "¿Quién soy?",
            target="sobremi",
        ),

    ],
    brand="COVID-19 en España (act. {})".format(
        dataset.last_update().strftime('%d/%m/%Y')),
    brand_href="/",
    color="primary",
    dark=True,
    fluid=True,
    sticky='top',
    style={'zIndex': '999'},
    className='d-sm-none d-lg-block'
)

nav_mob = dbc.NavbarSimple(
    children=[

        dbc.NavItem(dbc.NavLink("📈 Incrementos diarios",
                                id='tooltip-inc', href="incrementos")),
        dbc.NavItem(dbc.NavLink("🏠 Detalle comunidad",
                                id='tooltip-comunidad', href='comunidad')),
        dbc.NavItem(dbc.NavLink("🧾 Modelos matemáticos",
                                id='tooltip-modelos', href='modelos')),
        dbc.NavItem(
            dbc.NavLink("🧔",
                        id="open", href="#"), id='sobremi'
        ),
        dbc.Modal(
            [
                dbc.ModalHeader("Sobre este proyecto"),
                dbc.ModalBody(dcc.Markdown('''
                 Para el desarrollo del proyecto se han usado los datos publicados por [Datadista](https://github.com/datadista/datasets/tree/master/COVID%2019) y el GeoJSON de las comunidades autónomas de [Albert del Amor](https://albertdelamor.carto.com/tables/comunidades_autonomas_etrs89_30n/public/map).

                 El código desarrollado para este proyecto, así como otros Jupyter Notebooks usados para analizar el estado de los datos de la pandemia en España están disponibles en [el repositorio del proyecto](https://github.com/juanlurg/covid-19-spain-dash), en la web podrá encontrar artículos explicando paso a paso el desarrollo. Principalmente para este proyecto se ha usado Python con Dash, plotly y pandas.

                 Realizado por [**Juan Luis Ramirez**](https://github.com/juanlurg)
                 
                 Contacto: [**juanlu.rgarcia@gmail.com**](mailto:juanlu.rgarcia@gmail.com)
                ''')),
                dbc.ModalFooter(
                    dbc.Button("Cerrar", id="close", className="ml-auto")
                ),
            ],
            id="modal",
            centered=True
        ),
        dbc.Tooltip(
            "Visualice los incrementos diarios de contagios, fallecidos y recuperados",
            target="tooltip-inc",
        ),
        dbc.Tooltip(
            "Vista concreta del estado de cada comunidad",
            target="tooltip-comunidad",
        ),
        dbc.Tooltip(
            "Usando modelos matemáticos para predecir la evolución de la pandemia",
            target="tooltip-modelos",
        ),
        dbc.Tooltip(
            "¿Quién soy?",
            target="sobremi",
        ),

    ],
    brand="COVID-19 en España",
    brand_href="/",
    color="primary",
    dark=True,
    fluid=True,
    sticky='top',
    style={'zIndex': '999', 'height': '150px'},
    expand='lg',
    className='d-sm-block d-lg-none'
)
