import pandas as pd
from dash import Dash, dcc, html

# Load your dataset
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

# Initialize the app
app = Dash(__name__)

# Define the layout of the app
app.layout = html.Div(children=[
    html.H1(children='My First Dash App'),
    html.Div(children='''Dash: A web application framework for your data.'''),

    # Add a graph component
    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': df['continent'], 'y': df['lifeExp'], 'type': 'bar', 'name': 'Life Expectancy'},
            ],
            'layout': {
                'title': 'Life Expectancy by Continent'
            }
        }
    )
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
