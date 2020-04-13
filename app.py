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

FONT_AWESOME = "https://use.fontawesome.com/releases/v5.7.2/css/all.css"

app = dash.Dash(__name__, external_stylesheets=[
                dbc.themes.COSMO, FONT_AWESOME])


server = app.server

app.config.suppress_callback_exceptions = True
