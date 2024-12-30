import json

import dash
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html
from dash.dependencies import Input, Output, State

from data.get_data import get_dataframe_to_plot
from templates.description import description
from templates.header import header
from templates.plotting import plotting
from templates.sidebar import sidebar
from utils.constants import SCALE_OPTIONS

# Global variable to store the dataframe
df, cat_columns = get_dataframe_to_plot()

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.VAPOR],
    assets_folder="assets",
    prevent_initial_callbacks="initial_duplicate",
)
# Global variable to store the dataframe
df, cat_columns = get_dataframe_to_plot()

# Modal
with open("EXPLANATIONS.md", "r") as f:
    howto_md = f.read()

modal_overlay = dbc.Modal(
    [
        dbc.ModalBody(html.Div([dcc.Markdown(howto_md)], id="howto-md")),
        dbc.ModalFooter(dbc.Button("Close", id="howto-close", className="howto-bn")),
    ],
    id="modal",
    size="lg",
)
button_howto = dbc.Button(
    "Learn more",
    id="howto-open",
    outline=True,
    color="info",
    # Turn off lowercase transformation for class .button in stylesheet
    style={"textTransform": "none", "marginRight": "10px"},
)

button_github = dbc.Button(
    "View Code on github",
    outline=True,
    color="primary",
    href="https://github.com/rafal-mokrzycki/dash-pandas/",
    id="gh-link",
    style={"text-transform": "none"},
    target="_blank",
)


# Header
header = dbc.Navbar(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.Img(
                            id="logo",
                            src="assets/dash-logo-new.png",
                            height="30px",
                        ),
                        md="auto",
                    ),
                    dbc.Col(
                        [
                            html.Div(
                                [
                                    html.H3("Interactive Plots"),
                                    html.P("Economic data"),
                                ],
                                id="app-title",
                            )
                        ],
                        md=True,
                        align="center",
                    ),
                ],
                align="center",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.NavbarToggler(id="navbar-toggler"),
                            dbc.Collapse(
                                dbc.Nav(
                                    [
                                        dbc.NavItem(button_howto),
                                        dbc.NavItem(button_github),
                                    ],
                                    navbar=True,
                                ),
                                id="navbar-collapse",
                                navbar=True,
                            ),
                            modal_overlay,
                        ],
                        md=2,
                    ),
                ],
                align="center",
            ),
        ],
        fluid=True,
    ),
    dark=True,
    color="dark",
    sticky="top",
)

# Description
description = dbc.Col(
    [
        dbc.Card(
            id="description-card",
            children=[
                dbc.CardHeader("Explanation"),
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Img(
                                            src="assets/economic_data_img_example.png",
                                            width="200px",
                                        )
                                    ],
                                    md="auto",
                                ),
                                dbc.Col(
                                    html.P(
                                        "This is an example of an interactive economic data plotter that allows users to visualize two datasets through bar plots and scatter plots. "  # noqa: E501
                                        "Users can enhance their scatter plots by adding linear trendlines, providing valuable insights into data trends and relationships. "  # noqa: E501
                                        "The application offers customizable color schemes, enabling users to tailor the visual appearance of their plots to better suit their presentation needs. "  # noqa: E501
                                        "Additionally, users have the option to download their visualizations in multiple formats, including PNG, JPG, and SVG, ensuring compatibility with various applications and platforms. "  # noqa: E501
                                        "This tool aims to facilitate data analysis and improve the accessibility of economic data visualization for users of all skill levels. "  # noqa: E501
                                    ),
                                    md=True,
                                ),
                            ]
                        ),
                    ]
                ),
            ],
        )
    ],
    md=12,
)

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
                    html.H5(
                        "Select plot type",
                        className="card-title",
                    ),
                    dcc.Dropdown(
                        id="plot-type-selector",
                        options=PLOT_TYPES,
                        value="",  # TODO: choose
                        style={"color": "black"},
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


# Callback to update dataframe based on user selection
@app.callback(
    Output("x-axis-selector", "options", allow_duplicate=True),
    Output("y-axis-selector", "options", allow_duplicate=True),
    Output("x-axis-selector", "value", allow_duplicate=True),
    Output("y-axis-selector", "value", allow_duplicate=True),
    Input("dataset-selector", "value"),
)
def update_data_options(selected_dataset: str) -> tuple[list, list, str, str]:
    global df
    global cat_columns
    df, cat_columns = get_dataframe_to_plot(selected_dataset)

    # Generate options for x and y axis selectors based on dataframe columns
    x_options = [{"label": col, "value": col} for col in df.columns]
    y_options = [
        {"label": col, "value": col} for col in df.columns if col not in cat_columns
    ]

    return (
        x_options,
        y_options,
        x_options[0]["value"],
        y_options[0]["value"],
    )


# Combined callback for Y axis options and disabled state based on selected X axis
@app.callback(
    # Output("output-container", "children"),
    Output("x-axis-selector", "options", allow_duplicate=True),
    Output("y-axis-selector", "options", allow_duplicate=True),
    Output("x-axis-selector", "value", allow_duplicate=True),
    Output("y-axis-selector", "value", allow_duplicate=True),
    Input("dataset-selector", "value"),
)
def update_data_options(selected_dataset: str) -> tuple[list, list, str, str]:
    global df  # Declare df as global to modify it
    global cat_columns
    df, cat_columns = get_dataframe_to_plot(
        selected_dataset
    )  # Update df based on selection

    # Generate options for x and y axis selectors based on dataframe columns
    x_options = [{"label": col, "value": col} for col in df.columns]
    y_options = [
        {"label": col, "value": col} for col in df.columns if col not in cat_columns
    ]

    return (
        x_options,
        y_options,
        x_options[0]["value"],
        y_options[0]["value"],
    )


# Combined callback for Y axis options and disabled state based on selected X axis
@app.callback(
    Output("y-axis-selector", "options", allow_duplicate=True),
    Output("y-axis-selector", "disabled", allow_duplicate=True),
    Output("x-axis-scale", "options", allow_duplicate=True),
    Output("x-axis-scale", "value", allow_duplicate=True),
    Input("x-axis-selector", "value"),
)
def update_y_axis_variables_selection(x_axis: str) -> tuple[list, bool, list, bool]:
    if x_axis in cat_columns:
        return (
            [{"label": "", "value": ""}],
            True,
            [{"label": "Nominal", "value": "Nominal"}],
            "Nominal",
        )
    return (
        [{"label": col, "value": col} for col in df.columns if col not in cat_columns],
        False,
        SCALE_OPTIONS,
        "linear",
    )


# Callback to update graph and store its figure data
@app.callback(
    Output("graph-output", "figure"),
    Output("stored-figure", "data"),
    Input("x-axis-selector", "value"),
    Input("y-axis-selector", "value"),
    Input("x-axis-scale", "value"),
    Input("y-axis-scale", "value"),
    Input("color-theme-selector", "value"),
    Input("scatter-plot-trendline", "value"),
)
def update_graph(
    x_axis: str,
    y_axis: str,
    x_scale: str,
    y_scale: str,
    color_theme: str,
    trendline: list,
) -> tuple[go.Figure, str]:

    if x_axis in cat_columns:
        df_count = df[x_axis].value_counts().reset_index()
        df_count.columns = [x_axis, "count"]
        fig = px.bar(df_count, x=x_axis, y="count")
        if y_scale == "log":
            fig.update_yaxes(type="log")
        fig.update_layout(
            title=dict(text=f"Barplot: {x_axis}", font=dict(size=24)),
            title_x=0.5,
            xaxis_title=x_axis,
            yaxis_title="Count",
            template=color_theme,
        )
    else:
        if trendline:
            fig = px.scatter(
                df,
                x=x_axis,
                y=y_axis,
                text=x_axis,
                trendline="ols",
                trendline_color_override="red",
            )
        else:
            fig = px.scatter(df, x=x_axis, y=y_axis, text=x_axis)

        fig.update_traces(textposition="top center")
        fig.update_xaxes(type=x_scale)
        fig.update_yaxes(type=y_scale)
        fig.update_layout(
            title=dict(text=f"Scatterplot: {y_axis} vs. {x_axis}", font=dict(size=24)),
            title_x=0.5,
            xaxis_title=x_axis,
            yaxis_title=y_axis,
            template=color_theme,
        )

    return fig, fig.to_json()


# Callback to handle download requests using stored figure data
@app.callback(
    Output("download-image", "data"),
    Input("download-jpg", "n_clicks"),
    Input("download-png", "n_clicks"),
    Input("download-svg", "n_clicks"),
    State("stored-figure", "data"),
    prevent_initial_call=True,
)
def download_image(jpg_clicks, png_clicks, svg_clicks, stored_figure):
    if not stored_figure:
        return

    # Load the figure from JSON using plotly.graph_objects
    fig_dict = json.loads(stored_figure)
    fig = go.Figure(fig_dict)

    # Determine which button was clicked and save accordingly
    file_path = ""

    if jpg_clicks:
        file_path = "output_image.jpg"
        fig.write_image(file_path)
        return dcc.send_file(file_path)
    elif png_clicks:
        file_path = "output_image.png"
        fig.write_image(file_path)
        return dcc.send_file(file_path)
    elif svg_clicks:
        file_path = "output_image.svg"
        fig.write_image(file_path)
        return dcc.send_file(file_path)


# Callback for modal popup
@app.callback(
    Output("modal", "is_open"),
    [Input("howto-open", "n_clicks"), Input("howto-close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


# Callback to toggle the collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


# Callback for modal popup
@app.callback(
    Output("modal", "is_open"),
    [Input("howto-open", "n_clicks"), Input("howto-close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


# we use a callback to toggle the collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


# Run the app
if __name__ == "__main__":
    app.run(debug=True, port=8080)
