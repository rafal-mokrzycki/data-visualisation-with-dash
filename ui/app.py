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
        html.H1("Select Variables to Plot"),
        # Checkbox for selecting variables
        dcc.Checklist(
            id="variable-selector",
            options=[
                {"label": "Population", "value": "Population"},
                {"label": "Area", "value": "Area"},
                {"label": "GDP", "value": "GDP"},
            ],
            value=["Population"],  # Default selected variable
            inline=True,
        ),
        # Graph output
        dcc.Graph(id="graph-output"),
    ]
)


# Callback to update graph based on selected variables
@app.callback(Output("graph-output", "figure"), Input("variable-selector", "value"))
def update_graph(selected_variables):
    if not selected_variables:
        return px.line(title="Select variables to visualize data")

    # Create a bar chart based on selected variables
    fig = px.bar(df, x="Country", y=selected_variables, barmode="group")
    fig.update_layout(title="Selected Variables by Country")

    return fig


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
