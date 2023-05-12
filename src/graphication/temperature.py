import plotly.express as px
from dash import Dash, dcc, html, Input, Output

from src.data import data_consumption
import re

VACCINES = "VACCINES"


def box_plot():
    df = data_consumption.obtain_file_as_dataframe(
        file="Covid_Data.csv",
        directory="../../data/",
        delimiter=";"
    )

    # Initialize the app
    app = Dash(__name__)

    fig = px.box(df, x="State_age", y="temperature_average")

    app.layout = html.Div([
        html.H1(children='Covid deaths by date'),
        dcc.Graph(figure=fig, id="box_plot"),
    ])

    # Run the app
    if __name__ == '__main__':
        app.run_server(debug=True)


if __name__ == "__main__":
    box_plot()
