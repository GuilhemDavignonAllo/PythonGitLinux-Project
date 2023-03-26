import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import datetime

app = dash.Dash(__name__)
server = app.server

data = pd.read_csv('cleaneddata.csv', names=['timestamp', 'value'])
data['timestamp'] = pd.to_datetime(data['timestamp'])

app.layout = html.Div([
    dcc.Graph(id='time-series-graph'),
    html.Div(id='daily-report'),
    dcc.Interval(
        id='interval-component',
        interval=5*60*1000,  # in milliseconds
        n_intervals=0
    )
])

@app.callback(
    Output('time-series-graph', 'figure'),
    Input('interval-component', 'n_intervals'))
def update_time_series(n):
    data = pd.read_csv('cleaneddata.csv', names=['timestamp', 'value'])
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    fig = px.line(data, x='timestamp', y='value', title='Time Series of Values')
    return fig

@app.callback(
    Output('daily-report', 'children'),
    Input('interval-component', 'n_intervals'))
def update_daily_report(n):
    today = datetime.date.today()
    daily_data = data[data['timestamp'].dt.date == today]
    if daily_data.empty:
        return 'No data for today'
    else:
        open_price = daily_data['value'].iloc[0]
        close_price = daily_data['value'].iloc[-1]
        min_price = daily_data['value'].min()
        max_price = daily_data['value'].max()
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
