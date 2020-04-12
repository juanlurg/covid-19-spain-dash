# -*- coding: utf-8 -*-
import json
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_bootstrap_components as dbc
import numpy as np
import locale
import plotly.express as px
from dash.dependencies import Input, Output
import plotly.graph_objects as go

locale.setlocale(locale.LC_ALL, 'es_ES')


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LITERA])

file_data = 'https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/ccaa_covid19_datos_isciii.csv'

df = pd.read_csv(file_data)

df['Fecha'] = pd.to_datetime(df['Fecha'])
last_update = df['Fecha'].max()
last_update_str = last_update.strftime('%d de %B de %Y')
df_grouped = df.groupby('Fecha').sum()
infected = df_grouped['Casos'].iloc[-1].astype(np.int64)
deseased = df_grouped['Fallecidos'].iloc[-1].astype(np.int64)
recovered = df_grouped['Recuperados'].iloc[-1].astype(np.int64)
active_cases = infected - deseased - recovered

hoy = df[df['Fecha'] == last_update]
hoy['Casos Activos'] = hoy['Casos'] - hoy['Fallecidos'] - hoy['Recuperados']
hoy = hoy.drop(columns=['Hospitalizados', 'UCI'])

with open('../data/geo.json') as response:
    communities = json.load(response)


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
        dbc.NavItem(dbc.NavLink(
            "Datos actualizados el {}".format(last_update_str), href="#")),

    ],
    brand="COVID-19 en España",
    brand_href="#",
    color="primary",
    dark=True,
)


cards_content = []

for metric in metrics_dict:
    cards_content.append(
        dbc.Col(
            dbc.Card([
                dbc.CardHeader(metric),
                dbc.CardBody(
                    [
                        html.H5('{:n}'.format(metrics_dict[metric]),
                                className='card-title h1')
                    ]
                )],
                color=colors_dict[metric],
                inverse=True
            )
        )

    )

cards = html.Div(
    [
        dbc.Row(
            dbc.CardGroup(
                cards_content),
            className="mb-4",
            justify='center'
        ),
    ]
)

fig = [go.Choroplethmapbox(geojson=communities, locations=hoy['cod_ine'], z=hoy['Casos Activos'],
                           featureidkey='properties.codigo',
                           colorscale="OrRd", zmin=hoy['Casos Activos'].min(), zmax=hoy['Casos Activos'].max(),
                           marker_opacity=1, marker_line_width=0, showlegend=False, showscale=False
                           )
       ]


layout = go.Layout(mapbox_style="carto-positron",
                   mapbox_zoom=5, mapbox_center={"lat": 40.416775, "lon": -3.703790}, autosize=False,
                   width=500,
                   height=900,
                   margin=dict(
                       l=0,
                       r=0,
                       b=0,
                       t=0))


app.layout = dbc.Container(
    [
        navbar,
        html.Br(),
        cards,
        dcc.Graph(figure={"data": fig, "layout": layout}, responsive=True),
    ],
    fluid=True,
)


if __name__ == '__main__':
    app.run_server(debug=True)
