from dash import html
import dash_bootstrap_components as dbc
import components.pages.emissions as emissions_page


tabs = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        emissions_page.page
                    ], className="pt-3")
            ]),

        dbc.Row(
            [ 
                # dbc.Col(
                #     [
                        html.Hr(),
                        dbc.Col([
                            html.Span([html.P(['Source: ',  html.A(['2020 Annual Report from the European Commission on CO2 Emissions from Maritime Transport'], href='https://ec.europa.eu/clima/document/download/3eb00f74-c7ba-4dd1-8ea6-18f6f135053e_en')]),
                                   ])
                        ]),
                        dbc.Col([
                            html.Div([
                                html.Span('Powered by: RODA Technology'),
                                html.A(
                                    html.Img(src='../static/roda-logo-backup.png', style={'width': '70px', 'height': '30px', 'margin-left': '10px'}),
                                    href='https://rodatech.co.uk/',  # Link to redirect
                                ),
                            ], className = 'footer-container')
                        ])
                        
                    # ]),

            ]
        )
    ],
    fluid=True
)
