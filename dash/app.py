# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_bootstrap_components as dbc


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

file_data = 'https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/ccaa_covid19_datos_isciii.csv'

df = pd.read_csv(file_data)

df['Fecha'] = pd.to_datetime(df['Fecha'])
last_update = df['Fecha'].max()
last_update = last_update.strftime('%d de %B de %Y')
df_grouped = df.groupby('Fecha').sum()
infected = df_grouped['Casos'][-1:]
deseased = df_grouped['Fallecidos'][-1:]
recovered = df_grouped['Recuperados'][-1:]
active_cases = infected - deseased - recovered

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

cards = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(dbc.Card(card_content, color="primary", inverse=True)),
                dbc.Col(dbc.Card(card_content, color="secondary", inverse=True)),
                dbc.Col(dbc.Card(card_content, color="info", inverse=True)),
                dbc.Col(dbc.Card(card_content, color="secondary", inverse=True)),
            ],
            className="mb-4",
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
