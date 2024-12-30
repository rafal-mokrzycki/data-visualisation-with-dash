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

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.VAPOR],
    assets_folder="assets",
    prevent_initial_callbacks="initial_duplicate",
)
# Global variable to store the dataframe
df, cat_columns = get_dataframe_to_plot()


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
    # Output("x-axis-scale", "disabled", allow_duplicate=True),
    Input("x-axis-selector", "value"),
)
def update_y_axis_variables_selection(x_axis: str) -> tuple[list, bool, list, bool]:
    if x_axis in cat_columns:
        return (
            [{"label": "", "value": ""}],
            True,
            [{"label": "Nominal", "value": "Nominal"}],
            "Nominal",
        )  # Hide Y axis selector if categorical
    return (
        [{"label": col, "value": col} for col in df.columns if col not in cat_columns],
        False,
        SCALE_OPTIONS,
        "linear",
    )  # Show it otherwise


# Callback to update graph and store its figure data
@app.callback(
    Output("graph-output", "figure"),
    Output("stored-figure", "data"),  # Store figure data in JSON format
    Input("x-axis-selector", "value"),
    Input("y-axis-selector", "value"),
    Input("x-axis-scale", "value"),
    Input("y-axis-scale", "value"),
    Input("color-theme-selector", "value"),
    Input("scatter-plot-trendline", "value"),  # New input for trendline checkbox
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

    return fig, fig.to_json()  # Return style for checkbox visibility


# Callback to handle download requests using stored figure data
@app.callback(
    Output("download-image", "data"),
    Input("download-jpg", "n_clicks"),
    Input("download-png", "n_clicks"),
    Input("download-svg", "n_clicks"),
    State("stored-figure", "data"),  # Get stored figure data
    prevent_initial_call=True,
)
def download_image(jpg_clicks, png_clicks, svg_clicks, stored_figure):
    if not stored_figure:
        return

    # Load the figure from JSON using plotly.graph_objects
    fig_dict = json.loads(stored_figure)  # Convert JSON string back to dictionary
    fig = go.Figure(fig_dict)  # Create a Figure object from the dictionary

    # Determine which button was clicked and save accordingly
    file_path = ""

    if jpg_clicks:
        file_path = "output_image.jpg"
        fig.write_image(file_path)  # Save as JPG
        return dcc.send_file(file_path)  # Send file for download
    elif png_clicks:
        file_path = "output_image.png"
        fig.write_image(file_path)  # Save as PNG
        return dcc.send_file(file_path)  # Send file for download
    elif svg_clicks:
        file_path = "output_image.svg"
        fig.write_image(file_path)  # Save as SVG
        return dcc.send_file(file_path)  # Send file for download


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
