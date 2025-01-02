import plotly.graph_objects as go
import pytest
import repackage

repackage.up()
from app import (
    download_image,
    toggle_modal,
    toggle_navbar_collapse,
    update_both_axes_variables_selection_and_scale_options,
    update_data_options,
    update_graph,
)
from utils.constants import SCALE_OPTIONS


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            "housing data",
            (
                [
                    {"label": "price", "value": "price"},
                    {"label": "house_type", "value": "house_type"},
                    {"label": "sqft", "value": "sqft"},
                    {"label": "bedrooms", "value": "bedrooms"},
                    {"label": "bathrooms", "value": "bathrooms"},
                    {"label": "receptions", "value": "receptions"},
                    {"label": "location", "value": "location"},
                    {"label": "city", "value": "city"},
                ],
                [
                    {"label": "price", "value": "price"},
                    {"label": "sqft", "value": "sqft"},
                ],
                "price",
                "price",
            ),
        ),
    ],
)
def test_update_data_options(test_input, expected):
    # TODO: mock global df and global cat_columns
    output = update_data_options(test_input)
    assert output == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            "pie",
            (
                [{"label": "", "value": ""}],
                True,
                [{"label": "Nominal", "value": "Nominal"}],
                "Nominal",
            ),
        ),
        (
            "scatter",
            (
                [
                    {"label": "price", "value": "price"},
                    {"label": "sqft", "value": "sqft"},
                ],
                False,
                SCALE_OPTIONS,
                "linear",
            ),
        ),
    ],
)
def test_update_both_axes_variables_selection_and_scale_options(test_input, expected):
    output = update_both_axes_variables_selection_and_scale_options(test_input)
    assert output == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            ("price", "sqft", "linear", "linear", "ggplot2", True),
            (go.Figure, str),
        ),
    ],
)
def test_update_graph(test_input, expected):
    x_axis, y_axis, x_scale, y_scale, color_theme, trendline = test_input
    output = update_graph(x_axis, y_axis, x_scale, y_scale, color_theme, trendline)
    assert [type(i) for i in output] == [i for i in expected]


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ((False, False, True, None), "output_image.svg"),
        ((False, True, False, None), "output_image.png"),
        ((True, False, False, None), "output_image.jpg"),
    ],
)
def test_download_image(test_input, expected):
    # TODO: mock plot
    jpg, png, svg, data = test_input
    _, data = update_graph("price", "sqft", "linear", "linear", "ggplot2", True)
    output = download_image(jpg, png, svg, data)
    assert output["filename"] == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ((1, 1, True), False),
        ((1, 0, True), False),
        ((0, 1, True), False),
        ((0, 0, True), True),
        ((1, 1, False), True),
        ((1, 0, False), True),
        ((0, 1, False), True),
        ((0, 0, False), False),
    ],
)
def test_toggle_modal(test_input, expected):
    n1, n2, is_open = test_input
    output = toggle_modal(n1, n2, is_open)
    assert output is expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ((1, False), True),
        ((1, True), False),
        ((0, False), False),
        ((0, True), True),
    ],
)
def test_toggle_navbar_collapse_pos(test_input, expected):
    n, is_open = test_input
    output = toggle_navbar_collapse(n, is_open)
    assert output is expected
