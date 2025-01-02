import plotly.graph_objects as go

TITLE_FONT_SIZE = 24
TITLE_X_SIZE = 0.5


def update_plot_layouts(plot_type: str, fig: go.Figure, **kwargs):
    fig.update_layout(
        title=dict(text="", font=dict(size=TITLE_FONT_SIZE)),
        title_x=TITLE_X_SIZE,
        template=kwargs["color_theme"],
    )
    fig.update_xaxes(type=kwargs["x_scale"])
    fig.update_yaxes(type=kwargs["y_scale"])
    match plot_type:
        case "bar":
            fig.update_layout(
                title=dict(text=f"Barplot: {kwargs['x_axis']}"),
                xaxis_title=kwargs["x_axis"],
                yaxis_title="Count",
            )
        case "pie":
            fig.update_layout(
                title=dict(text=f"Pie chart: {kwargs['x_axis']}"),
                xaxis_title="",
                yaxis_title="",
            )
        case "box":
            if kwargs["x_axis"] is None:

                fig.update_layout(
                    title=dict(
                        text=f"Box Plot: distribution of {kwargs['y_axis']}",
                    ),
                    yaxis_title=f"Distribution of {kwargs['y_axis']}",
                )
            else:
                fig.update_layout(
                    title=dict(
                        text=f"Box Plot: distribution of {kwargs['y_axis']} by categories of {kwargs['x_axis']}",  # noqa: E501
                    ),
                    xaxis_title=f"Categories of {kwargs['x_axis']}",
                    yaxis_title=f"Distribution of {kwargs['y_axis']}",
                )
        case "scatter":
            fig.update_traces(textposition="top center")
            fig.update_layout(
                title=dict(
                    text=f"Scatterplot: {kwargs['y_axis']} vs. {kwargs['x_axis']}",
                ),
                xaxis_title=kwargs["x_axis"],
                yaxis_title=kwargs["y_axis"],
            )
        case "histogram":
            fig.update_layout(
                title=dict(
                    text=f"Histogram: Distribution of {kwargs['x_axis']}",
                ),
                xaxis_title="Value",
                yaxis_title="Count",
            )
