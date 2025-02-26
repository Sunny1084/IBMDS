import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

# Load SpaceX launch data
df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")

# Create a Dash app
app = dash.Dash(__name__)

# TASK 1: Add a Launch Site Drop-down Input Component
app.layout = html.Div([
    html.H1("SpaceX Launch Dashboard", style={'textAlign': 'center'}),
    dcc.Dropdown(
        id='site-dropdown',
        options=[{'label': 'All Sites', 'value': 'ALL'}] +
                [{'label': site, 'value': site} for site in df['Launch Site'].unique()],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    html.Br(),
    
    # TASK 2: Add a callback function to render success-pie-chart based on selected site dropdown
    dcc.Graph(id='success-pie-chart'),
    html.Br(),
    
    # TASK 3: Add a Range Slider to Select Payload
    dcc.RangeSlider(
        id='payload-slider',
        min=0, max=10000, step=1000,
        marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
        value=[df['Payload Mass (kg)'].min(), df['Payload Mass (kg)'].max()]
    ),
    html.Br(),
    
    # TASK 4: Add a callback function to render the success-payload-scatter-chart scatter plot
    dcc.Graph(id='success-payload-scatter-chart')
])

# Callback for TASK 2: Pie Chart
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(df, values='class', names='Launch Site', title='Total Success Launches')
    else:
        filtered_df = df[df['Launch Site'] == entered_site]
        fig = px.pie(filtered_df, names='class', title=f'Success vs. Failure for {entered_site}')
    return fig

# Callback for TASK 4: Scatter Plot
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'), Input('payload-slider', 'value')]
)
def update_scatter_chart(entered_site, payload_range):
    filtered_df = df[(df['Payload Mass (kg)'] >= payload_range[0]) & (df['Payload Mass (kg)'] <= payload_range[1])]
    
    if entered_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
    
    fig = px.scatter(
        filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version',
        title='Correlation between Payload and Success for Selected Site'
    )
    return fig

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
