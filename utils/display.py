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
