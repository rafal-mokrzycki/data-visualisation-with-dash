import dash_bootstrap_components as dbc
from dash import html

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
