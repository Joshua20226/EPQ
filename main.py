from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import os
from components.tabs import tabs
from components.navbar import navbar
import flask

app = Dash(__name__)
server = app.server 

# Set app title
app.title = 'Shipping Dashboard'

# Create flask route for static images
STATIC_PATH = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'static')

@app.server.route('/static/<resource>')
def serve_static(resource):
    return flask.send_from_directory(STATIC_PATH, resource)

app.layout = html.Div(
    children=[
        navbar, 
        tabs
    ]
)

app.index_string = """<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>"""


if __name__ == '__main__':
    app.run_server(debug=True, host='localhost')