# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Div(dcc.Dropdown(list(pd.unique(spacex_df['Launch Site'])), list(pd.unique(spacex_df['Launch Site'])), multi=True, id='site-dropdown')),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                html.Div(dcc.RangeSlider(min_payload, max_payload, value=[min_payload, max_payload], id='payload-slider')),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart'))
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output("success-pie-chart", "figure"), 
    Input("site-dropdown", "value"))
def generate_chart(sites):
    values = []
    if len(sites) > 1:
        for s in sites:
            values.append(len(spacex_df[(spacex_df['Launch Site'] == s) & (spacex_df['class'] == 1)]))
        names = sites
    else:
        values.append(len(spacex_df[(spacex_df['Launch Site'] == sites[0]) & (spacex_df['class'] == 1)]))
        values.append(len(spacex_df[(spacex_df['Launch Site'] == sites[0]) & (spacex_df['class'] == 0)]))
        names = ['success', 'failure']
    fig = px.pie(values=values, names=names)
    fig.update_layout(title='Total Success Launches by site')
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output("success-payload-scatter-chart", "figure"), 
    Input("site-dropdown", "value"),
    Input("payload-slider", "value"))
def generate_chart2(sites, payload):
    filtered = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload[0]) & (spacex_df['Payload Mass (kg)'] <= payload[1])]
    x = filtered['Payload Mass (kg)']
    y = filtered['class']
    fig = px.scatter(x=x, y=y, color=filtered['Booster Version Category'])
    fig.update_layout(title='Correlation betweeen Pyload and success for all sites', xaxis_title='Payload (kg)', yaxis_title='class')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
