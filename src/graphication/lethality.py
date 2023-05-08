import plotly.express as px
from dash import Dash, html, dcc

from src.data import data_consumption


def lethality_graph():
    df = data_consumption.obtain_file_as_dataframe(
        file="Covid_Data.csv",
        directory="../../data/",
        delimiter=";"
    )

    # Initialize the app
    app = Dash(__name__)

    # App layout
    app.layout = html.Div([
        html.Div(children='Covid data visualization'),
        dcc.Graph(figure=px.pie(df, names='Final_state', title='Population of European continent'))
    ])

    # Run the app
    if __name__ == '__main__':
        app.run_server(debug=True)


if __name__ == "__main__":
    lethality_graph()
