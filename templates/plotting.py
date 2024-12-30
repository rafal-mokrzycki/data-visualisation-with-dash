import dash_bootstrap_components as dbc
from dash import dcc, html

# Data Plotting
plotting = [
    dbc.Card(
        id="plotting-card",
        children=[
            dbc.CardHeader("Viewer"),
            dbc.CardBody(
                [
                    html.Div(
                        [
                            # Graph output
                            dcc.Graph(id="graph-output"),
                            dcc.Store(id="stored-figure"),
                        ]
                    ),
                ]
            ),
            dbc.CardFooter(
                [
                    html.H5(
                        "Download as:",
                        className="card-title",
                    ),
                    dbc.Button(
                        "JPG",
                        id="download-jpg",
                        className="btn btn-light",
                        outline=True,
                    ),
                    dbc.Button(
                        "PNG",
                        id="download-png",
                        className="btn btn-light",
                        outline=True,
                    ),
                    dbc.Button(
                        "SVG",
                        id="download-svg",
                        className="btn btn-light",
                        outline=True,
                    ),
                    dcc.Download(id="download-image"),
                ],
                style={
                    "display": "inline",
                },
            ),
        ],
    )
]
