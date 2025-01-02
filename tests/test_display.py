import plotly.graph_objects as go
import pytest
import repackage

repackage.up()
from utils.display import update_plot_layouts


@pytest.fixture
def fig():
    """Fixture to create a new Plotly figure for testing."""
    return go.Figure()


@pytest.mark.parametrize(
    "plot_type, x_axis, y_axis, x_scale, y_scale, color_theme, expected_title, expected_x_title, expected_y_title",  # noqa: E501
    [
        (
            "bar",
            "Category",
            None,
            "linear",
            "linear",
            "plotly",
            "Barplot: Category",
            "Category",
            "Count",
        ),
        (
            "pie",
            "Category",
            None,
            "linear",
            "linear",
            "plotly",
            "Pie chart: Category",
            "",
            "",
        ),
        (
            "box",
            "Category",
            "Value",
            "linear",
            "linear",
            "plotly",
            "Box Plot: distribution of Value by categories of Category",
            "Categories of Category",
            "Distribution of Value",
        ),
        (
            "box",
            None,
            "Value",
            "linear",
            "linear",
            "plotly",
            "Box Plot: distribution of Value",
            None,
            "Distribution of Value",
        ),
        (
            "scatter",
            "X Value",
            "Y Value",
            "linear",
            "linear",
            "plotly",
            "Scatterplot: Y Value vs. X Value",
            "X Value",
            "Y Value",
        ),
        (
            "histogram",
            "Value",
            None,
            "linear",
            "linear",
            "plotly",
            "Histogram: Distribution of Value",
            "Value",
            "Count",
        ),
    ],
)
def test_update_plot_layouts(
    fig,
    plot_type,
    x_axis,
    y_axis,
    x_scale,
    y_scale,
    color_theme,
    expected_title,
    expected_x_title,
    expected_y_title,
):
    kwargs = {
        "x_axis": x_axis,
        "y_axis": y_axis,
        "color_theme": color_theme,
        "x_scale": x_scale,
        "y_scale": y_scale,
    }

    update_plot_layouts(plot_type, fig, **kwargs)

    assert fig.layout.title.text == expected_title
    assert fig.layout.xaxis.title.text == expected_x_title
    assert fig.layout.yaxis.title.text == expected_y_title


# Run the tests with pytest
if __name__ == "__main__":
    pytest.main()
