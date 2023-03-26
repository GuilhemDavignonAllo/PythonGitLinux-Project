import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Event
import plotly.graph_objs as go
import os
import subprocess
import time

# Define the path to the CSV file
csv_path = '/home/GuilhemDavignonAllo/PythonGitLinux-Project/cleaneddata.csv'

# Create a Dash app
app = dash.Dash(__name__)

# Define the layout of the dashboard
app.layout = html.Div(children=[
    html.H1(children='TSLA Stock Prices Dashboard'),
    dcc.Graph(id='tsla-stock-prices-graph'),
    dcc.Interval(id='interval-component', interval=5*60*1000, n_intervals=0),
    html.Div(id='latest-price')
])

# Define the callback function to update the graph with new data
@app.callback(Output('tsla-stock-prices-graph', 'figure'),
              [Event('interval-component', 'interval')])
def update_graph(interval):
    # Read the CSV file to get the data
    df = pd.read_csv(csv_path, parse_dates=['timestamp'])

    # Create a line chart of TSLA stock prices over time
    data = [go.Scatter(x=df['timestamp'], y=df['price'])]
    layout = go.Layout(title='TSLA Stock Prices', xaxis={'title': 'Timestamp'}, yaxis={'title': 'Price'})
    figure = go.Figure(data=data, layout=layout)

    return figure

# Define the callback function to display the latest price
@app.callback(Output('latest-price', 'children'),
              [Event('interval-component', 'interval')])
def update_latest_price(interval):
    # Read the CSV file to get the data
    df = pd.read_csv(csv_path, parse_dates=['timestamp'])

    # Get the latest price
    latest_price = df['price'].iloc[-1]

    return f'Latest price: {latest_price}'

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

