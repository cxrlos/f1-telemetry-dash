import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from urllib.request import urlopen
import json
from datetime import datetime

# Initialize the Dash app
app = dash.Dash(__name__)

# URL for the API endpoint
url = "https://api.openf1.org/v1/car_data?driver_number=81&session_key=9158"

# Function to fetch and process data
def fetch_data():
    response = urlopen(url)
    data = json.loads(response.read())
    df = pd.DataFrame(data)
    
    # Convert date string to datetime
    df['date'] = pd.to_datetime(df['date'])
    
    return df

# App layout
app.layout = html.Div([
    html.H1('F1 Brake Telemetry - Driver 81'),
    
    dcc.Graph(
        id='brake-telemetry',
        style={'height': '70vh'}
    ),
    
    html.Div([
        html.P('Data refreshes automatically every 10 seconds'),
        dcc.Interval(
            id='interval-component',
            interval=10*1000,  # in milliseconds
            n_intervals=0
        )
    ])
], style={'padding': '20px'})

# Callback to update the graph
@app.callback(
    Output('brake-telemetry', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_graph(n):
    df = fetch_data()
    
    fig = px.line(
        df,
        x='date',
        y='brake',
        title='Brake Application Over Time',
        labels={
            'date': 'Time',
            'brake': 'Brake Application (%)'
        }
    )
    
    fig.update_layout(
        xaxis_title='Time',
        yaxis_title='Brake Application (%)',
        yaxis=dict(range=[0, 100]),
        hovermode='x unified'
    )
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)