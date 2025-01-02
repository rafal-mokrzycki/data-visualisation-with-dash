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
from utils.constants import SCALE_OPTIONS, SCALE_OPTIONS_BOTH_DISABLED

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
    y_options = [{"label": col, "value": col} for col in df.columns]

    return (
        x_options,
        y_options,
        x_options[0]["value"],
        y_options[0]["value"],
    )


@app.callback(
    Output("x-axis-selector", "options", allow_duplicate=True),
    Output("x-axis-selector", "value", allow_duplicate=True),
    Output("y-axis-selector", "options", allow_duplicate=True),
    Output("y-axis-selector", "value", allow_duplicate=True),
    Output("y-axis-selector", "disabled", allow_duplicate=True),
    Output("x-axis-scale", "options", allow_duplicate=True),
    Output("y-axis-scale", "options", allow_duplicate=True),
    Input("plot-type-selector", "value"),
)
def update_both_axes_variables_selection_and_scale_options(
    plot_type: str,
) -> tuple[list, bool, list, bool]:
    if plot_type == "bar":
        x_columns = [
            {"label": col, "value": col} for col in df.columns if col in cat_columns
        ]
        y_columns = [{"label": "(plot only one variable)", "value": "no_value"}]
        y_disabled = False
        x_scale = SCALE_OPTIONS_BOTH_DISABLED
        y_scale = SCALE_OPTIONS

    elif plot_type == "pie":
        x_columns = [
            {"label": col, "value": col} for col in df.columns if col in cat_columns
        ]
        y_columns = [{"label": "", "value": ""}]
        y_disabled = True
        x_scale = SCALE_OPTIONS_BOTH_DISABLED
        y_scale = SCALE_OPTIONS_BOTH_DISABLED

    elif plot_type == "box":  # TODO: fix for different boxplots types
        x_columns = [{"label": col, "value": col} for col in df.columns]
        y_columns = [{"label": col, "value": col} for col in df.columns]
        y_disabled = False
        x_scale = SCALE_OPTIONS_BOTH_DISABLED
        y_scale = SCALE_OPTIONS
    elif plot_type == "histogram":
        x_columns = [
            {"label": col, "value": col} for col in df.columns if col not in cat_columns
        ]
        y_columns = [{"label": "", "value": ""}]
        y_disabled = False
        x_scale = SCALE_OPTIONS_BOTH_DISABLED
        y_scale = SCALE_OPTIONS

    elif plot_type == "scatter":
        x_columns = [
            {"label": col, "value": col} for col in df.columns if col not in cat_columns
        ]
        y_columns = [
            {"label": col, "value": col} for col in df.columns if col not in cat_columns
        ]
        y_disabled = False
        x_scale = SCALE_OPTIONS
        y_scale = SCALE_OPTIONS

    else:
        raise ValueError("Something went wrong.")
    return (
        x_columns,
        x_columns[0]["value"],
        y_columns,
        y_columns[0]["value"],
        y_disabled,
        x_scale,
        y_scale,
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
    Input("plot-type-selector", "value"),
)
def update_graph(
    x_axis: str,
    y_axis: str,
    x_scale: str,
    y_scale: str,
    color_theme: str,
    trendline: list,
    plot_type: str,
) -> tuple[go.Figure, str]:
    if plot_type == "bar":  # and x_axis in cat_columns:
        # bar plot (1 variable - categorical)
        df_count = df[x_axis].value_counts().reset_index()
        df_count.columns = [x_axis, "count"]
        fig = px.bar(df_count, x=x_axis, y="count")
        fig.update_yaxes(type=y_scale)
        fig.update_layout(
            title=dict(text=f"Barplot: {x_axis}", font=dict(size=24)),
            title_x=0.5,
            xaxis_title=x_axis,
            yaxis_title="Count",
            template=color_theme,
        )
    elif plot_type == "pie":
        # pie plot (1 variable - categorical)
        df_grouped = df.groupby(x_axis).size().reset_index(name="count")

        fig = px.pie(
            df_grouped,
            names=x_axis,
            values="count",
        )

        fig.update_layout(
            title=dict(text=f"Pie chart: {x_axis}", font=dict(size=24)),
            title_x=0.5,
        )
    elif plot_type == "box" and x_axis in cat_columns and y_axis not in cat_columns:
        # box plot (2 variables - categorical + continuous)
        fig = px.box(
            df,
            x=x_axis,  # Categorical variable for x-axis
            y=y_axis,  # Numerical variable for y-axis
            # color="y_axis",  # Categorical variable for color differentiation
        )

        fig.update_yaxes(type=y_scale)

        fig.update_layout(
            title=dict(
                text="Box Plot: Value Distribution by Categories",
                font=dict(size=24),
            ),
            title_x=0.5,
            xaxis_title=f"Categories ({x_axis})",
            yaxis_title=f"Distribution of {y_axis}",
        )

    elif plot_type == "box" and x_axis not in cat_columns:
        #  plot (1 variable - continuous)
        fig = px.box(
            df,
            y=x_axis,
        )

        fig.update_yaxes(type=y_scale)

        fig.update_layout(
            title=dict(
                text=f"Box Plot: Distribution of {x_axis}",
                font=dict(size=24),
            ),
            title_x=0.5,
            yaxis_title=f"Distribution of {x_axis}",
        )
    elif plot_type == "scatter":
        # scatter plot (2 variables - continuous + continuous)
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
    elif plot_type == "histogram":
        # histogram (1 variable - continuous)
        fig = px.histogram(
            df,
            x=x_axis,
            title=f"Histogram of {x_axis}",
            labels={"value": x_axis},
            nbins=10,
        )
        fig.update_yaxes(type=y_scale)

        fig.update_layout(
            title=dict(
                text="Histogram: Distribution of Continuous Variable",
                font=dict(size=24),
            ),
            title_x=0.5,
            xaxis_title="Value",
            yaxis_title="Count",
        )

    else:
        raise ValueError("Wrong plot type.")
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


# Run the app
if __name__ == "__main__":
    app.run(debug=True, port=8080)
