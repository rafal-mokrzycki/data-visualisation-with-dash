import dash
import dash_bootstrap_components as dbc
from dash import html

from templates.description import description
from templates.header import header
from templates.plotting import plotting
from templates.sidebar import sidebar
from utils.callbacks import get_callbacks

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.VAPOR],
    assets_folder="assets",
    prevent_initial_callbacks="initial_duplicate",
)


app.layout = html.Div(
    [
        header,
        dbc.Container(
            [
                dbc.Row(description),
                dbc.Row(
                    id="app-content",
                    children=[dbc.Col(plotting, md=8), dbc.Col(sidebar, md=4)],
                ),
            ],
            fluid=True,
        ),
    ]
)
get_callbacks(app)


# Run the app
if __name__ == "__main__":
    app.run(debug=True, port=8080)
