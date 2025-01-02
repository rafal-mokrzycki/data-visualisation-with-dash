import plotly.graph_objects as go


def update_plot_layouts(
    plot_type: str,
    fig: go.Figure,
    x_axis: str,
    y_axis: str,
    x_scale: str,
    y_scale: str,
    color_theme: str,
):
    fig.update_yaxes(type=y_scale)
    match plot_type:
        case "bar":
            fig.update_layout(
                title=dict(text=f"Barplot: {x_axis}", font=dict(size=24)),
                title_x=0.5,
                xaxis_title=x_axis,
                yaxis_title="Count",
                template=color_theme,
            )
