import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app, server
from apps import app1, app2, app3, app4

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])
app.title = 'Datos de España - COVID-19'

server = app.server
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/incrementos':
        return app2.page
    elif pathname == '/comunidad':
        return app3.page
    elif pathname == '/modelos':
        return app4.page
    else:
        return app1.page


if __name__ == '__main__':
    app.run_server(debug=False)
