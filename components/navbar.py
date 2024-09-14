from dash import html
import dash_bootstrap_components as dbc

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src='/static/logo_processed.png',
                                height="30px"), class_name='navbar-brand'),
                    ],
                    align="center",
                ),
                style={"textDecoration": "none"},
            ),
            dbc.Col(html.Div("Shipping Dashboard", className="page-header")),
            html.Span(className="spacer"),
            dbc.Button("Learn More", className="page-button", color="light"),
        ],
        fluid=True,
    ),
    color="#0D2C7A",
    dark=True,
    class_name="navbar-tbl"
)
