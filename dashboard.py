from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import pandas as pd

df = pd.read_csv("cleaneddata.csv")

app = Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='TSLA Stock Prices Dashboard'),
    dcc.Graph(id='tsla-stock-prices-graph'),
    dcc.Interval(id='interval-component', interval=5*60*1000, n_intervals=0),
    html.Div(id='latest-price')
])

@app.callback(
    Output('tsla-stock-prices-graph', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_graph(n):
    data = {
        'x': df['timestamp'],
        'y': df['price'],
        'type': 'line',
        'name': 'TSLA'
    }
    return {'data': [data]}

if __name__ == '__main__':
    app.run_server(host = '0.0.0.0',port=8050)

