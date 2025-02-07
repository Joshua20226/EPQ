
import threading
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
global output_list, group_ship_type_list, ships_by_type_list, df1_list, carbon_emission_lines, carbon_cost_lines, group_ship_type_huge_list, df1_huge_list, carbon_emission_lines_list, carbon_cost_lines_list

output_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
group_ship_type_huge_list = []
df1_huge_list = []
carbon_emission_lines_list = []
carbon_cost_lines_list = []
emission_fig = 0
cost_fig = 0

def get_df(path):
    df = pd.read_excel(path)
    return df

def create_df_list(group_ship_type_list, ships_by_type_list, df1_list, df, price):
    group_ship_type = df.groupby(by='Ship type').sum(numeric_only=True).reset_index()
    group_ship_type.sort_values(
        by='Total CO₂ emissions [m tonnes]', ascending=False, inplace=True)
    group_ship_type['Implied carbon cost'] = group_ship_type['Total CO₂ emissions [m tonnes]'] * price

    group_ship_type_list.append(group_ship_type)

    ships_by_type = df.groupby(by='Ship type').count()
    ships_by_type.reset_index(inplace=True)
    ships_by_type = ships_by_type.iloc[:, :2]
    ships_by_type.columns = ['Ship type', 'Number of ships']
    ships_by_type.sort_values(by='Number of ships',
                              ascending=False, inplace=True)
    
    ships_by_type_list.append(ships_by_type)

    # total_emissions
    total_emissions_by_type = df.groupby(by='Ship type').sum(numeric_only=True)
    total_emissions_by_type.reset_index(inplace=True)
    total_emissions_by_type = total_emissions_by_type.loc[:, [
        'Ship type', 'Total CO₂ emissions [m tonnes]']]

    df1 = ships_by_type.merge(total_emissions_by_type, on='Ship type')

    # Calc emissions per ship
    df1['Emissions per ship'] = df1['Total CO₂ emissions [m tonnes]'] / \
        df1['Number of ships']

    carbon_price = price
    # Calc cost per ship
    df1['Cost per ship'] = df1['Emissions per ship'] * carbon_price

    # Sort on cost per ship
    df1.sort_values(by='Cost per ship', ascending=False, inplace=True)
    
    df1_list.append(df1)
    
def implied_carbon_cost_graph(group_ship_type_list, year_options, type_options):
    
    for i, df in enumerate(group_ship_type_list):
        df['Year'] = year_options[i] 
        
    combined_df = pd.concat(group_ship_type_list)
    # filtering the ship types
    combined_df = combined_df[combined_df['Ship type'].isin(type_options)]
    
    ship_types = combined_df['Ship type'].unique()
    year_options = sorted(combined_df['Year'].unique())

    colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A']  # Example colors
    colors = ['#0D2C7A', '#00429d', '#157dec', '#3d7ceb', '#6fa1f8', '#ABCAFF']
    color_map = {str(year): color for year, color in zip(year_options, colors)}
    
    # Map ship types to numeric values
    ship_type_to_numeric = {ship_type: i for i, ship_type in enumerate(ship_types)}

    fig = go.Figure()
    bar_width = 0.5
    group_spacing = 0.5

    # Calculate the offset to center the ticks
    tick_offset = ((len(year_options) - 1) * bar_width) / 2


    # Iterate over each year and ship type to add bars to the figure
    for year in year_options:
        year_df = combined_df[combined_df['Year'] == year]
        for i, ship_type in enumerate(ship_types):
            df_filtered = year_df[year_df['Ship type'] == ship_type]
            text_for_hover = ['{:,.2f}m tonnes'.format(i/1000000) for i in df_filtered['Total CO₂ emissions [m tonnes]']]
            if not df_filtered.empty:
                # Get the text for the current bar

                x_pos = ship_type_to_numeric[ship_type] * (len(year_options) * bar_width + group_spacing) + (year_options.index(year) * bar_width)
                
                # Add the bar with a custom hovertemplate
                fig.add_trace(go.Bar(
                    x=[x_pos],
                    y=df_filtered['Implied carbon cost'],
                    width=bar_width,
                    marker_color=color_map[str(year)],
                    name=str(year),
                    text=text_for_hover,  # Set the bar text (visible on the bar)
                    hoverinfo='text',  # Specify that only text is displayed on hover
                    hovertemplate=str(text_for_hover).strip("'[]") + f'<br>Year: {year}<extra></extra>',  # Custom hover template
                    legendgroup=str(year),
                    showlegend=i == 0
                ))
                
    fig.update_traces(textfont=dict(size=16))  # Set the size to your preference

    # Update the layout to use numeric x-axis and custom tick labels
    fig.update_layout(
        xaxis = {
            'tickmode': 'array',
            'tickvals': [ship_type_to_numeric[st] * (len(year_options) * bar_width + group_spacing) + tick_offset for st in ship_types],
            'ticktext': ship_types
        },
        yaxis=dict(title='Implied Carbon Cost'),
        yaxis_range=[0, combined_df['Implied carbon cost'].max() * 1.1],
        barmode='group',
        legend_title=dict(text='Year'),
    )
    
    return fig

def ships_by_type_graph(ships_by_type_list, year_options, type_options):
    for i, df in enumerate(ships_by_type_list):
        df['Year'] = year_options[i] 
        
    combined_df = pd.concat(ships_by_type_list)
    # filtering the ship types
    combined_df = combined_df[combined_df['Ship type'].isin(type_options)]
    
    ship_types = combined_df['Ship type'].unique()
    year_options = sorted(combined_df['Year'].unique())

    colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A']  # Example colors
    colors = ['#0D2C7A', '#00429d', '#157dec', '#3d7ceb', '#6fa1f8', '#ABCAFF']
    color_map = {str(year): color for year, color in zip(year_options, colors)}
    
    # Map ship types to numeric values
    ship_type_to_numeric = {ship_type: i for i, ship_type in enumerate(ship_types)}

    sbt_fig = go.Figure()
    bar_width = 0.5
    group_spacing = 0.5

    # Calculate the offset to center the ticks
    tick_offset = ((len(year_options) - 1) * bar_width) / 2


    # Iterate over each year and ship type to add bars to the figure
    for year in year_options:
        year_df = combined_df[combined_df['Year'] == year]
        for i, ship_type in enumerate(ship_types):
            df_filtered = year_df[year_df['Ship type'] == ship_type]
            if not df_filtered.empty:
                # Get the text for the current bar

                x_pos = ship_type_to_numeric[ship_type] * (len(year_options) * bar_width + group_spacing) + (year_options.index(year) * bar_width)
                
                # Add the bar with a custom hovertemplate
                sbt_fig.add_trace(go.Bar(
                    x=[x_pos],
                    y=df_filtered['Number of ships'],
                    width=bar_width,
                    marker_color=color_map[str(year)],
                    name=str(year),
                    legendgroup=str(year),
                    showlegend=i == 0
                ))
                
    sbt_fig.update_traces(textfont=dict(size=16))  # Set the size to your preference

    # Update the layout to use numeric x-axis and custom tick labels
    sbt_fig.update_layout(
        xaxis = {
            'tickmode': 'array',
            'tickvals': [ship_type_to_numeric[st] * (len(year_options) * bar_width + group_spacing) + tick_offset for st in ship_types],
            'ticktext': ship_types
        },
        yaxis=dict(title='Number of ships'),
        yaxis_range=[0, combined_df['Number of ships'].max() * 1.1],
        barmode='group',
        legend_title=dict(text='Year'),
    )
    return sbt_fig

def cpv_fig_graph(df1_list, year_options, type_options):    
    for i, df in enumerate(df1_list):
        df['Year'] = year_options[i] 
        
    combined_df = pd.concat(df1_list)
    # filtering the ship types
    combined_df = combined_df[combined_df['Ship type'].isin(type_options)]
    
    ship_types = combined_df['Ship type'].unique()
    year_options = sorted(combined_df['Year'].unique())

    colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A']  # Example colors
    colors = ['#0D2C7A', '#00429d', '#157dec', '#3d7ceb', '#6fa1f8', '#ABCAFF']
    color_map = {str(year): color for year, color in zip(year_options, colors)}
    
    # Map ship types to numeric values
    ship_type_to_numeric = {ship_type: i for i, ship_type in enumerate(ship_types)}

    cpv_fig = go.Figure()
    bar_width = 0.5
    group_spacing = 0.5

    # Calculate the offset to center the ticks
    tick_offset = ((len(year_options) - 1) * bar_width) / 2


    # Iterate over each year and ship type to add bars to the figure
    for year in year_options:
        year_df = combined_df[combined_df['Year'] == year]
        for i, ship_type in enumerate(ship_types):
            df_filtered = year_df[year_df['Ship type'] == ship_type]
            if not df_filtered.empty:
                # Get the text for the current bar

                x_pos = ship_type_to_numeric[ship_type] * (len(year_options) * bar_width + group_spacing) + (year_options.index(year) * bar_width)
                
                # Add the bar with a custom hovertemplate
                cpv_fig.add_trace(go.Bar(
                    x=[x_pos],
                    y=df_filtered['Cost per ship'],
                    width=bar_width,
                    marker_color=color_map[str(year)],
                    name=str(year),
                    legendgroup=str(year),
                    showlegend=i == 0
                ))
                
    cpv_fig.update_traces(textfont=dict(size=16))  # Set the size to your preference

    # Update the layout to use numeric x-axis and custom tick labels
    cpv_fig.update_layout(
        xaxis = {
            'tickmode': 'array',
            'tickvals': [ship_type_to_numeric[st] * (len(year_options) * bar_width + group_spacing) + tick_offset for st in ship_types],
            'ticktext': ship_types
        },
        yaxis=dict(title='Cost per ship'),
        yaxis_range=[0, combined_df['Cost per ship'].max() * 1.1],
        barmode='group',
        legend_title=dict(text='Year'),
    )
    cpv_fig.update_yaxes(tickprefix="£")
    
    return cpv_fig

def bars_full_data(price, index):
    global group_ship_type_list, ships_by_type_list, df1_list, group_ship_type_huge_list, df1_huge_list

    # group ship
    paths = ['./data/filtered_2018-v270-11102023-EU MRV Publication of information.xlsx', './data/filtered_2019-v217-11102023-EU MRV Publication of information.xlsx', 
            './data/filtered_2020-v109-25012023-EU.xlsx', './data/filtered_2021-v195-28032024-EU MRV Publication of information.xlsx', './data/filtered_2022-v177-27032024-EU MRV Publication of information.xlsx', 
            './data/filtered_2023-v15-25092024-EU MRV Publication of information.xlsx']

    group_ship_type_list = []
    ships_by_type_list = []
    df1_list = []

    for path in paths:
        df = get_df(path)
        create_df_list(group_ship_type_list, ships_by_type_list, df1_list, df, price)
    
    # price filtered
    group_ship_type_huge_list.append(group_ship_type_list)
    df1_huge_list.append(df1_list)
    
    group_ship_type = group_ship_type_list[-1]
    carbon_price = price
    text_price = '£{:,.0f}'.format(carbon_price)
    group_ship_type['Implied carbon cost'] = group_ship_type['Total CO₂ emissions [m tonnes]'] * carbon_price

    group_ship_carbon_cost = group_ship_type['Implied carbon cost'].sum()/1000000000

    # total_emissions
    total_emissions = group_ship_type['Total CO₂ emissions [m tonnes]'].sum()
    total_emissions_text = f"{total_emissions/1000000:,.0f}m"

    total_emissions_price = total_emissions * carbon_price
    total_emissions_price_text = f"£{total_emissions_price/1000000000:,.1f}bn"

    # if 'Ro-pax ship' in type_options:
    roPax = group_ship_type[group_ship_type['Ship type'] ==
                            "Ro-pax ship"]['Total CO₂ emissions [m tonnes]'].values[0]
    roPax_price = roPax*price/1000000000
    roPax_shr = roPax / total_emissions * price

    effic = df.groupby(by='Ship type').mean(numeric_only=True).reset_index()
    effic = effic.sort_values(
        by='Annual average Fuel consumption per distance [kg / n mile]', ascending=True)

    # Cost per ship
    total_emissions_by_type = df.groupby(by='Ship type').sum(numeric_only=True)
    total_emissions_by_type.reset_index(inplace=True)

    total_emissions_by_type = total_emissions_by_type.loc[:, [
        'Ship type', 'Total CO₂ emissions [m tonnes]']]
    
    output_list[index] = [text_price, group_ship_carbon_cost, roPax_shr, roPax_price, effic, total_emissions_text, total_emissions_price_text]
    # return 
    
def bars_graphs(group_ship_type_list, ships_by_type_list, df1_list, year_options, type_options, price):
    
    # filtering years by findinig the index of the year_options in years then
    # get the corresponding index from the df lists into a filtered list
    years = ['2018', '2019', '2020', '2021', '2022', '2023']
    year_index_list = []
    filtered_group_ship_type_list = []
    filtered_ships_by_type_list = []
    filtered_df1_list = []
    
    for year in years:
        if year in year_options:
            year_index_list.append(years.index(year))
    
    # filtering year
    for index in range(len(group_ship_type_list)):
        if index in year_index_list:
            filtered_group_ship_type_list.append(group_ship_type_list[index])
            filtered_ships_by_type_list.append(ships_by_type_list[index])
            filtered_df1_list.append(df1_list[index])
            
    if len(filtered_group_ship_type_list) != 0:
        colors = ['#0D2C7A'] * (len(filtered_group_ship_type_list[0]))
        colors[1] = '#D17A22'
        
        # fig graph for grouped bar chart
        fig = implied_carbon_cost_graph(filtered_group_ship_type_list, year_options, type_options)
        sbt_fig = ships_by_type_graph(filtered_ships_by_type_list, year_options, type_options)
        cpv_fig = cpv_fig_graph(filtered_df1_list, year_options, type_options)
    else:
        fig = go.Scatter(x=[], y=[])
        sbt_fig = go.Scatter(x=[], y=[])
        cpv_fig = go.Scatter(x=[], y=[])

    return fig, sbt_fig, cpv_fig

    

def time_series_full_df(price):
    global carbon_emission_lines_list, carbon_cost_lines_list
    
    carbon_emission_lines = {}
    carbon_cost_lines = {}
    carbon_price = price

    # read the df and append data of all ship types to a separate list for each ship type
    def data_to_multiple_lists(path, carbon_emission_lines, carbon_cost_lines):
        df = pd.read_excel(path)
    
        group_ship_type = df.groupby(by='Ship type').sum(numeric_only=True).reset_index()
        group_ship_type.sort_values(
            by='Total CO₂ emissions [m tonnes]', ascending=False, inplace=True)
        
        for carbon_emission in group_ship_type['Total CO₂ emissions [m tonnes]']:
            ship_type = group_ship_type.loc[group_ship_type.index[group_ship_type['Total CO₂ emissions [m tonnes]'] == carbon_emission].tolist()[0], ['Ship type']].values[0]
            
            if ship_type in carbon_emission_lines:
                carbon_emission_lines[ship_type].append(round(carbon_emission, 2))
                carbon_cost_lines[ship_type].append(round(carbon_emission * carbon_price, 2))
            else:
                carbon_emission_lines[ship_type] = [round(carbon_emission, 2)]
                carbon_cost_lines[ship_type] = [round(carbon_emission * carbon_price, 2)]
    
    paths = ['./data/filtered_2018-v270-11102023-EU MRV Publication of information.xlsx', './data/filtered_2019-v217-11102023-EU MRV Publication of information.xlsx', 
             './data/filtered_2020-v109-25012023-EU.xlsx', './data/filtered_2021-v195-28032024-EU MRV Publication of information.xlsx', './data/filtered_2022-v177-27032024-EU MRV Publication of information.xlsx', 
             './data/filtered_2023-v15-25092024-EU MRV Publication of information.xlsx']
    
    for path in paths:
        data_to_multiple_lists(path, carbon_emission_lines, carbon_cost_lines)

    carbon_emission_lines_list.append(carbon_emission_lines)
    carbon_cost_lines_list.append(carbon_cost_lines)
    
def time_series_graph(carbon_emission_lines, carbon_cost_lines, type_options):
    emission_data = {
        'date' : pd.date_range(start='2018-01-01', end='2023-12-31', freq='YS')[:6],
    }
    
    for ship in carbon_emission_lines: 
        if ship in type_options:
            emission_data[ship] = carbon_emission_lines[ship]

    colors = ['#0D2C7A', '#1A5276', '#2874A6', '#3498DB', '#5DADE2',
            '#7FB3D5', '#AED6F1', '#D6EAF8', '#A9CCE3', '#7FB3D5',
            '#5499C7', '#2980B9', '#1F618D', '#154360', '#21618C']
    
    emission_df = pd.DataFrame(emission_data)
    emission_fig = px.line(emission_df, x='date', y=[ship_type for ship_type in carbon_emission_lines if ship_type in type_options], color_discrete_sequence=colors)
    emission_fig.update_layout(
        xaxis_title='',
        yaxis_title="Carbon Emissions",
        yaxis_range=[0, max(max(carbon_emission_lines.values(), default=[])) * 1.1],
        legend=dict(
            orientation="h",
            xanchor="center",
            x=0.5,
            y=-0.2
        ),
        legend_title_text='Ship Types',
        autosize=True
    )
    
    cost_data = {
        'date' : pd.date_range(start='2018-01-01', end='2023-12-31', freq='YS')[:6],
    }
    for ship in carbon_cost_lines:
        if ship in type_options:
            cost_data[ship] = carbon_cost_lines[ship]

    cost_df = pd.DataFrame(cost_data)
    cost_fig = px.line(cost_df, x='date', y=[ship_type for ship_type in carbon_cost_lines if ship_type in type_options], color_discrete_sequence=colors)
    cost_fig.update_layout(
        xaxis_title='',
        yaxis_title="Carbon Cost",
        yaxis_range=[0, max(max(carbon_cost_lines.values(), default=[])) * 1.1],
        legend=dict(
            orientation="h",
            xanchor="center",
            x=0.5,
            y=-0.2
        ),
        legend_title_text='Ship Types',
        autosize=True
    )
    return emission_fig, cost_fig

def main():
    global group_ship_type_list, ships_by_type_list, df1_list, group_ship_type_huge_list
    
    start_time = time.time()
    num_threads_running = threading.active_count()
    # print("Number of threads currently running:", num_threads_running)
    # if num_threads_running <= 2:
    prices = [50, 70, 85, 105, 120, 140, 155, 175, 190, 200]
    for price in prices:
        # print('started a thread')
        bars_full_data(price, prices.index(price))
        time_series_full_df(price)


    # print(len(group_ship_type_huge_list))
    # emission_fig, cost_fig = time_series_full_df(price, type_options)
    # fig, text_price, group_ship_carbon_cost, roPax_shr, roPax_price, effic, sbt_fig, cpv_fig, total_emissions_text, total_emissions_price_text = bars_full_data(price, year_options, type_options)
    end_time = time.time()
    # print(str(end_time - start_time), 's')
    
# main()
