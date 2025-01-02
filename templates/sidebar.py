import dash_bootstrap_components as dbc
import repackage
from dash import dcc, html

from data.get_data import get_dataframe_to_plot

repackage.up()
from utils.constants import DATASET_OPTIONS, PLOT_THEMES, PLOT_TYPES, SCALE_OPTIONS

# Global variable to store the dataframe
df, cat_columns = get_dataframe_to_plot()

# Sidebar
sidebar = [
    dbc.Card(
        id="sidebar-card",
        children=[
            dbc.CardHeader("Tools"),
            dbc.CardBody(
                [
                    html.H5(
                        "Select dataset",
                        className="card-title",
                    ),
                    dcc.Dropdown(
                        id="dataset-selector",
                        options=DATASET_OPTIONS,
                        value="Housing Data",
                        style={"color": "black"},
                    ),
                    html.H5(
                        "Select plot type",
                        className="card-title",
                    ),
                    dcc.Dropdown(
                        id="plot-type-selector",
                        options=PLOT_TYPES,
                        value="scatter",
                        style={"color": "black"},
                    ),
                    # Title for selecting variables with spacing
                    html.H5(
                        "Select variables",
                        className="card-title",
                    ),
                    # Dropdown to select variables
                    html.Div(
                        [
                            # Dropdown to select X variable
                            html.Div(
                                [
                                    dcc.Dropdown(
                                        id="x-axis-selector",
                                        options=[
                                            {"label": col, "value": col}
                                            for col in df.columns
                                        ],
                                        value=df.columns.values.tolist()[0],
                                    ),
                                ],
                                style={
                                    "width": "48%",
                                    "display": "inline-block",
                                    "marginRight": "10px",
                                    "float": "left",
                                    "color": "black",
                                },
                            ),
                            # Dropdown to select Y variable
                            html.Div(
                                [
                                    dcc.Dropdown(
                                        id="y-axis-selector",
                                        options=[
                                            {"label": col, "value": col}
                                            for col in df.columns
                                            if col not in cat_columns
                                        ],
                                        value=df[
                                            df.columns.difference(cat_columns)
                                        ].columns.values.tolist()[
                                            0
                                        ],  # Default value
                                    ),
                                ],
                                style={
                                    "width": "48%",
                                    "display": "inline-block",
                                    "color": "black",
                                },
                            ),
                        ],
                        style={
                            "display": "inline",
                        },
                    ),  # Checkbox to select trendline
                    html.Div(
                        [
                            dcc.Checklist(
                                id="scatter-plot-trendline",
                                options=[
                                    {"label": "Show Trendline", "value": "trendline"}
                                ],
                                value=[],  # Default value (unchecked)
                                inputStyle={"marginRight": "5px"},
                            ),
                        ]
                    ),
                    html.Div(
                        dbc.Accordion(
                            [
                                dbc.AccordionItem(
                                    [  # Title for selecting scale with spacing
                                        html.H5(
                                            "Select scale",
                                            className="card-title",
                                        ),
                                        # Checkboxes for selecting axes scales
                                        html.Div(
                                            [
                                                # Checkbox for selecting X axis scale
                                                html.Div(
                                                    [
                                                        dcc.RadioItems(
                                                            id="x-axis-scale",
                                                            options=SCALE_OPTIONS,
                                                            value="linear",
                                                            inputStyle={
                                                                "marginRight": "5px",
                                                                "color": "white",
                                                            },
                                                        )
                                                    ],
                                                    style={
                                                        "width": "48%",
                                                        "display": "inline-block",
                                                        "marginRight": "10px",
                                                        "float": "left",
                                                    },
                                                ),
                                                # Checkbox for selecting Y axis scale
                                                html.Div(
                                                    [
                                                        dcc.RadioItems(
                                                            id="y-axis-scale",
                                                            options=SCALE_OPTIONS,
                                                            value="linear",
                                                            inputStyle={
                                                                "marginRight": "5px",
                                                            },
                                                        )
                                                    ],
                                                    style={
                                                        "width": "48%",
                                                        "display": "inline-block",
                                                    },
                                                ),
                                            ],
                                            style={
                                                "display": "inline",
                                            },
                                        ),
                                        # Title for selecting color theme with spacing
                                        html.H5(
                                            "Select color theme",
                                            className="card-title",
                                        ),
                                        # Dropdown for selecting the plot color theme
                                        dcc.Dropdown(
                                            id="color-theme-selector",
                                            options=[
                                                {"label": theme, "value": theme}
                                                for theme in PLOT_THEMES
                                            ],
                                            value="plotly",  # Default value
                                            style={
                                                "marginBottom": "20px",
                                                "color": "black",
                                            },
                                        ),
                                    ],
                                    title="Advanced options",
                                )
                            ],
                            flush=True,
                            start_collapsed=True,
                            style={"marginTop": "20px"},
                        )
                    ),
                ]
            ),
        ],
    ),
]
