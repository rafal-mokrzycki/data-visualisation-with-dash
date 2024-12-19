import dash
import pandas as pd
import plotly.express as px
from dash import Input, Output, dcc, html

# Sample data
df = pd.DataFrame(
    {
        "Country": ["USA", "Canada", "Germany", "UK", "France"],
        "Population": [331, 38, 83, 67, 65],
        "Area": [9833517, 9984670, 357022, 243610, 551695],
        "GDP": [21137518, 1848270, 3845630, 2825208, 2715518],
    }
)

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div(
    [
        html.H1("Select Variables for X and Y Axes"),
        # Dropdown to select variables
        html.Div(
            [
                html.Div(
                    [
                        html.Label("X Axis"),
                        dcc.Dropdown(
                            id="x-axis-selector",
                            options=[
                                {"label": col, "value": col}
                                for col in df.columns
                                # if col != "Country"
                            ],
                            value="Population",  # Default value
                        ),
                    ],
                    style={"width": "48%", "display": "inline-block"},
                ),
                html.Div(
                    [
                        html.Label("Y Axis"),
                        dcc.Dropdown(
                            id="y-axis-selector",
                            options=[
                                {"label": col, "value": col}
                                for col in df.columns
                                if col != "Country"
                            ],
                            value="GDP",  # Default value
                        ),
                    ],
                    style={"width": "48%", "display": "inline-block"},
                ),
            ]
        ),
        # Graph output
        dcc.Graph(id="graph-output"),
    ]
)


# Callback to update graph based on selected axes
@app.callback(
    Output("graph-output", "figure"),
    Input("x-axis-selector", "value"),
    Input("y-axis-selector", "value"),
)
def update_graph(x_axis, y_axis):
    # Check if the X axis is set to 'Country'
    if x_axis == "Country":
        # Create a bar plot if 'Country' is selected for the X axis
        fig = px.bar(df, x="Country", y=y_axis)
        fig.update_layout(
            title=f"{y_axis} by Country", xaxis_title="Country", yaxis_title=y_axis
        )
    else:
        # Create a scatter plot for other selections
        fig = px.scatter(df, x=x_axis, y=y_axis, text="Country")
        fig.update_traces(textposition="top center")  # Show country names on the points
        fig.update_layout(
            title=f"{y_axis} vs {x_axis}", xaxis_title=x_axis, yaxis_title=y_axis
        )

    return fig


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
