import pandas as pd
import plotly
from plotly import express as px
from plotly import graph_objs as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import datetime

# Load the data from the csv file
df = pd.read_csv('/home/GuilhemDavignonAllo/Project/data.csv', names=['date', 'price'])

# Create the app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1('Bitcoin Price'),
    dcc.Graph(id='graph'),
    html.Div(id='daily-report'),
    dcc.Interval(
        id='interval-component',
        interval=5*60*1000, # update every 5 minutes
        n_intervals=0
    )
])

# Define the callback to update the graph
@app.callback(Output('graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph(n):
    data = pd.read_csv('/home/GuilhemDavignonAllo/Project/data.csv',  names=['date', 'price'])
    fig = px.line(data, x='date', y='price', title='Time Series of Val')
    return fig

@app.callback(
    Output('daily-report', 'children'),
    Input('interval-component', 'n_intervals'))

def update_daily_report(n):
      
    df['date'] = pd.to_datetime(df['date'])
    today = datetime.date.today()
    daily_data = df[df['date'].dt.date == today]
    if daily_data.empty:
        return 'No data for today'
    else:
        open_price = daily_data['price'].iloc[0]
        close_price = daily_data['price'].iloc[-1]
        min_price = daily_data['price'].min()
        max_price = daily_data['price'].max()
        daily_volatility = max_price - min_price

        # Create a table to display the daily report
        table = html.Table([
            html.Tr([html.Th('Daily Report', colSpan=2)]),
            html.Tr([html.Td('Open Price:'), html.Td(open_price)]),
            html.Tr([html.Td('Close Price:'), html.Td(close_price)]),
            html.Tr([html.Td('Min Price:'), html.Td(min_price)]),
            html.Tr([html.Td('Max Price:'), html.Td(max_price)]),
            html.Tr([html.Td('Daily Volatility:'), html.Td(daily_volatility)])
        ])
        return table


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050)
