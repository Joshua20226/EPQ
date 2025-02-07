from sys import prefix
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, callback
from preload_resource import bars_graphs, time_series_graph

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))

@callback(
    Output('carbon_price', 'figure'),
    Output('carbon_price_paragraph', 'children'),
    Output('total_emissions', 'children'),
    Output('total_cost', 'children'),
    Output('sbt_fig', 'figure'),
    Output('cpv_fig', 'figure'),
    Output('emission_fig', 'figure'),
    Output('cost_fig', 'figure'),
    [Input('price_slider', 'value'),
     Input('year_checklist', 'value'),
     Input('type_checklist', 'value')]
)

def update_carbon_price(price, year_options, type_options):
    from preload_resource import group_ship_type_huge_list, carbon_cost_lines_list, carbon_emission_lines_list, ships_by_type_list, df1_huge_list, output_list

    # get result from preload_resource.py
    prices = [50, 70, 85, 105, 120, 140, 155, 175, 190, 200]
    text_price, group_ship_carbon_cost, roPax_shr, roPax_price, effic, total_emissions_text, total_emissions_price_text = output_list[prices.index(price)]
    fig, sbt_fig, cpv_fig = bars_graphs(group_ship_type_huge_list[prices.index(price)], ships_by_type_list, df1_huge_list[prices.index(price)], year_options, type_options, price)
    emission_fig, cost_fig = time_series_graph(carbon_emission_lines_list[prices.index(price)], carbon_cost_lines_list[prices.index(price)], type_options)

    paragraph = f'''At a price of {text_price} per kg of CO2 emissions, the cost of the carbon emissions from shipping activity will total £{group_ship_carbon_cost:,.1f}B.
    Ro-pax vessels, which account for {roPax_shr:,.0f}% of shipping carbon emissions, will attract a carbon price of £{roPax_price:,.1f}B. The most efficient class of vessel is the {effic['Ship type'].values[0]} with an annual average fuel consumption of
        {effic['Annual average Fuel consumption per distance [kg / n mile]'].values[0]:,.0f} kg/n mile, while the most expensive class of vessel is the {effic['Ship type'].values[-1]} with an average fuel
        consumption of {effic['Annual average Fuel consumption per distance [kg / n mile]'].values[-1]:.0f} kg/n mile. '''

    return fig, paragraph, total_emissions_text, total_emissions_price_text, sbt_fig, cpv_fig, emission_fig, cost_fig


page = html.Div(
    [
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H1("Putting a Global Price on Carbon",
                            className="display-4"),
                    html.Span(className="smallDividerLeft mb-2"),
                    html.P("There are clear indications from international climate change negotiations that the number of national, regional and sectoral carbon markets will dramatically increase over the next decade, as regulators turn to the market as the most cost effective mechanism to control GHGs.")
                ], sm=12, md=6),
                dbc.Col([
                    html.Div([
                        html.Div(className="stat-text m-0",
                                 id="total_emissions"),
                        html.H6("Total Emissions", className="stat-title m-0"),
                    ], className="stat"),
                ], sm=6, md=3),
                dbc.Col([
                    html.Div([
                        html.Div(className="stat-text m-0", id="total_cost"),
                        html.H6("Shipping Exposure to Carbon Price",
                                className="stat-title m-0"),
                    ], className="stat"),
                ], sm=6, md=3),
            ]),
            
            dbc.Row([
                html.Br(),
                html.Br(),

                html.Div([
                    dbc.Col([
                        html.H6("Ship type filter:"),
                        dcc.Dropdown(
                            id='type_checklist',
                            options=[
                                {'label': 'Passenger ship', 'value': 'Passenger ship'},
                                {'label': 'Ro-pax ship', 'value': 'Ro-pax ship'},
                                {'label': 'LNG carrier', 'value': 'LNG carrier'},
                                {'label': 'Container ship', 'value': 'Container ship'},
                                {'label': 'Ro-ro ship', 'value': 'Ro-ro ship'},
                                {'label': 'Container/ro-ro cargo ship', 'value': 'Container/ro-ro cargo ship'},
                                {'label': 'Refrigerated cargo carrier', 'value': 'Refrigerated cargo carrier'},
                                {'label': 'Combination carrier', 'value': 'Combination carrier'},
                                {'label': 'Oil tanker', 'value': 'Oil tanker'},
                                {'label': 'Other ship types', 'value': 'Other ship types'},
                                {'label': 'Gas carrier', 'value': 'Gas carrier'},
                                {'label': 'Chemical tanker', 'value': 'Chemical tanker'},
                                {'label': 'General cargo ship', 'value': 'General cargo ship'},
                                {'label': 'Bulk carrier', 'value': 'Bulk carrier'}
                            ],
                            value=['Passenger ship', 'Ro-pax ship', 'LNG carrier', 'Container ship', 'Ro-ro ship'],
                            multi=True,
                            # style={'padding-right': '10px'},
                            # className='custom-checkbox'
                        )
                        # , style={'margin-right': '100px'}
                    ], width=6, style={'margin-right': '180px', 'margin-left': '30px'}),
                    dbc.Col([
                        html.H6("Year filter:"),
                        dcc.Dropdown(
                            id='year_checklist',
                            options=[
                                {'label': '2018', 'value': '2018'},
                                {'label': '2019', 'value': '2019'},
                                {'label': '2020', 'value': '2020'},
                                {'label': '2021', 'value': '2021'},
                                {'label': '2022', 'value': '2022'}, 
                                {'label': '2023', 'value': '2023'}
                            ],
                            value=['2018', '2019', '2020', '2021', '2022', '2023'],
                            multi=True,
                            style={
                                'height': 'auto',
                                'minHeight': '20px',  # Reduce the minimum height as needed
                                'lineHeight': '20px',  # Adjust line height to fit the content
                            },
                            className='my-custom-dropdown'
                        ),
                    ], width=2.5)                    
                ], style={'display': 'flex'}),
            ]),

            dbc.Row([
                html.Br(),
                html.Br(),
                dbc.Col([
                    html.H6('Carbon emissions by vessel type over years', style={'margin-right': 'auto', 'margin-left': '30px', 'textAlign': 'center', 'margin-bottom': '0'}),
                    dcc.Graph(id='emission_fig', animate=True, style={'height': '70vh', 'width': '100%'})                    
                ], className = 'time-series-container', width=6),
                dbc.Col([
                    html.H6('Carbon cost by vessel type over years', style={'margin-right': 'auto', 'margin-left': '30px', 'textAlign': 'center', 'margin-bottom': '0'}),
                    dcc.Graph(id='cost_fig', animate=True, style={'height': '70vh', 'width': '100%'})                        
                ], className = 'time-series-container', width=6),
            ], style={'margin-top': '50px'}),

            dbc.Row([
                dbc.Col([
                    html.H3("What if?"),
                    html.P("Use the TBL shipping dashboard to explore how the price of carbon will impact the shipping industry, the national economy, and the environment.")
                ])
            ]),


            dbc.Row([

                dbc.Col([
                    html.Div([
                        html.B("Price per Tonne of Carbon Emissions (£)"),
                        dcc.Slider(50, 200, 35,
                                   value=50,
                                   id='price_slider',
                                   updatemode='drag'
                                   ), ], className="p-3",)
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H6("The Carbon Cost of Shipping"),
                        html.P(id='carbon_price_paragraph'),
                    ], className="p-3",)
                ], md=3, sm=12),
                dbc.Col([
                    html.H6("Implied carbon cost by vessel type, 2020 (£B)"),
                    dcc.Graph(id='carbon_price', animate=True)
                ], className="p-3", md=9, sm=12),
            ]),

            dbc.Row([
                dbc.Col([
                    html.H6("Number of ships by type"),
                    dcc.Graph(id='sbt_fig', animate=True)
                ], md=6, sm=12),
                dbc.Col([
                    html.H6("Carbon cost per vessel"),
                    dcc.Graph(id='cpv_fig', animate=True)
                ], md=6, sm=12),
            ]),
        ],
            fluid=True,
            className="m-3",
        ),

    ]


)
