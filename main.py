from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import os
from components.navbar import navbar

app = Dash(__name__)
server = app.server 

# Set app title
app.title = 'Shipping Dashboard'

# Create flask route for static images
STATIC_PATH = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'static')

app.layout = html.Div(
    children=[
        navbar
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
    app.run_server(debug=True, host='192.168.0.158')