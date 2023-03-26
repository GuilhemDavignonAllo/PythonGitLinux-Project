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
    html.H1('Tesla Stock Price'),
    dcc.Graph(id='time-series-graph'),
    html.Div([
        html.H2('Rapport Quotidien'),
        html.Table([
            html.Tr([html.Th('Date'), html.Th('Prix d\'ouverture'), html.Th('Prix de clôture'), html.Th('Prix minimal'), html.Th('Prix maximal'), html.Th('Volatilité quotidienne')]),
            html.Tr([html.Td(id='date'), html.Td(id='open-price'), html.Td(id='close-price'), html.Td(id='min-price'), html.Td(id='max-price'), html.Td(id='daily-volatility')])
        ])
    ], style={'margin': '50px'})
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
    [Output('date', 'children'),
     Output('open-price', 'children'),
     Output('close-price', 'children'),
     Output('min-price', 'children'),
     Output('max-price', 'children'),
     Output('daily-volatility', 'children')],
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

        return f'''
        Daily Report:
        Open Price: {open_price}
        Close Price: {close_price}
        Min Price: {min_price}
        Max Price: {max_price}
        Daily Volatility: {daily_volatility}
        '''

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050)
