from dash import html
import dash_bootstrap_components as dbc

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src='/static/logo.png',
                                height="30px"), class_name='navbar-brand'),
                        dbc.Col(html.Div("Shipping Dashboard", className="page-header")),
                    ],
                    align="center",
                ),
                # style={"textDecoration": "none"},
            ),
        ],
        fluid=True,
    ),
    color="#0D2C7A",
    dark=True,
    class_name="navbar-tbl"
)
