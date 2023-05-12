import plotly.express as px
from dash import Dash, dcc, html, Input, Output

from src.data import data_consumption
import re

VACCINES = "VACCINES"


def time_graph():
    df = data_consumption.obtain_file_as_dataframe(
        file="Covid_Data.csv",
        directory="../../data/",
        delimiter=";"
    )

    # Initialize the app
    app = Dash(__name__)

    df["Date_death_recovery"] = df["Date_death_recovery"].apply(lambda date: re.findall("^\d{4}-\d{2}", date)[0])
    a = df.groupby(["Date_death_recovery", "Final_state"])
    group = df.groupby(["Date_death_recovery", "Final_state"]).size().reset_index(name='Count')
    print(group)

    fig = px.bar(group, x="Date_death_recovery", y="Count", color='Final_state')

    # App layout
    app.layout = html.Div([
        html.H1(children='Covid deaths by date'),
        dcc.Graph(figure=fig, id="bubble_graph"),
    ])

    # Run the app
    if __name__ == '__main__':
        app.run_server(debug=True)


if __name__ == "__main__":
    time_graph()
