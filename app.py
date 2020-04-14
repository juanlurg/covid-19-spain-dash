# -*- coding: utf-8 -*-
import dash
import dash_bootstrap_components as dbc

FONT_AWESOME = "https://use.fontawesome.com/releases/v5.7.2/css/all.css"

app = dash.Dash(__name__, external_stylesheets=[
                dbc.themes.COSMO, FONT_AWESOME])


server = app.server

app.config.suppress_callback_exceptions = True
