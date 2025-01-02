import plotly.graph_objects as go


def update_plot_layouts(plot_type: str, fig: go.Figure, **kwargs):

    fig.update_yaxes(type=kwargs["y_scale"])
    match plot_type:
        case "bar":
            fig.update_layout(
                title=dict(text=f"Barplot: {kwargs['x_axis']}", font=dict(size=24)),
                title_x=0.5,
                xaxis_title=kwargs["x_axis"],
                yaxis_title="Count",
                template=kwargs["color_theme"],
            )
        case "pie":
            fig.update_layout(
                title=dict(text=f"Pie chart: {kwargs['x_axis']}", font=dict(size=24)),
                title_x=0.5,
            )
        case "box":
            if kwargs["x_axis"] is None:
                fig.update_yaxes(type=kwargs["y_scale"])

                fig.update_layout(
                    title=dict(
                        text=f"Box Plot: distribution of {kwargs['y_axis']}",
                        font=dict(size=24),
                    ),
                    title_x=0.5,
                    yaxis_title=f"Distribution of {kwargs['y_axis']}",
                )
            else:
                fig.update_yaxes(type=kwargs["y_scale"])

                fig.update_layout(
                    title=dict(
                        text=f"Box Plot: distribution of {kwargs['y_axis']} by categories of {kwargs['x_axis']}",
                        font=dict(size=24),
                    ),
                    title_x=0.5,
                    xaxis_title=f"Categories of {kwargs['x_axis']}",
                    yaxis_title=f"Distribution of {kwargs['y_axis']}",
                )
        case "scatter":
            fig.update_traces(textposition="top center")
            fig.update_xaxes(type=kwargs["x_scale"])
            fig.update_yaxes(type=kwargs["y_scale"])
            fig.update_layout(
                title=dict(
                    text=f"Scatterplot: {kwargs['y_axis']} vs. {kwargs['x_axis']}",
                    font=dict(size=24),
                ),
                title_x=0.5,
                xaxis_title=kwargs["x_axis"],
                yaxis_title=kwargs["y_axis"],
                template=kwargs["color_theme"],
            )
        case "histogram":
            fig.update_yaxes(type=kwargs["y_scale"])
            fig.update_layout(
                title=dict(
                    text="Histogram: Distribution of Continuous Variable",
                    font=dict(size=24),
                ),
                title_x=0.5,
                xaxis_title="Value",
                yaxis_title="Count",
            )
