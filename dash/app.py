# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_bootstrap_components as dbc
import numpy as np
import locale
locale.setlocale(locale.LC_ALL, 'es_ES')


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

file_data = 'https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/ccaa_covid19_datos_isciii.csv'

df = pd.read_csv(file_data)

df['Fecha'] = pd.to_datetime(df['Fecha'])
last_update = df['Fecha'].max()
last_update = last_update.strftime('%d de %B de %Y')
df_grouped = df.groupby('Fecha').sum()
infected = df_grouped['Casos'].iloc[-1].astype(np.int64)
deseased = df_grouped['Fallecidos'].iloc[-1].astype(np.int64)
recovered = df_grouped['Recuperados'].iloc[-1].astype(np.int64)
active_cases = infected - deseased - recovered

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
            "Datos actualizados el {}".format(last_update), href="#")),

    ],
    brand="COVID-19 en España",
    brand_href="#",
    color="primary",
    dark=True,
)

card_content = [
    dbc.CardBody(
        [
            html.H5("8000", className="card-title h1"),
            html.P(
                "INFECTADOS",
                className="card-text",
            ),
        ]
    ),
]

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

app.layout = dbc.Container(
    [
        navbar,
        html.Br(),
        cards
    ],
    fluid=True,
)

if __name__ == '__main__':
    app.run_server(debug=True)
