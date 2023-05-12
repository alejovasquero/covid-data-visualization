import plotly.express as px
from dash import Dash, dcc, html, Input, Output

from src.data import data_consumption

VACCINES = "VACCINES"


def lethality_graph():
    df = data_consumption.obtain_file_as_dataframe(
        file="Covid_Data.csv",
        directory="../../data",
        delimiter=";"
    )

    # Initialize the app
    app = Dash(__name__)

    filters_dict = dict({"age_range": f'Age > {30} & Age < {50}'})

    metadata = calculate_metadata(df)
    pie_view = "LETHALITY"

    # App layout
    app.layout = html.Div([
        html.H1(children='Covid data visualization'),
        dcc.Graph(figure=px.pie(df, names="Final_state", title='Covid data chart'), id="pie_graph"),
        html.H3(children="Age range"),
        dcc.RangeSlider(0, 100, 1, value=[30, 50], id='age_slider'),
        html.H3(children="Vaccine brand"),
        dcc.Dropdown(metadata[VACCINES], None, id='vaccine_brand'),
        html.H3(children="View"),
        dcc.Dropdown(["LETHALITY", "LOCATION"], None, id='pie_view'),
    ])

    @app.callback(
        Output("pie_graph", "figure", allow_duplicate=True),
        Input("age_slider", "value"),
        prevent_initial_call=True)
    def age_filter(age_range):
        nonlocal pie_view

        low_value, upper_range = age_range[0], age_range[1]
        filters_dict["age_range"] = f'Age > {low_value} & Age < {upper_range}'
        return calculate_graph(
            filters=filters_dict,
            original_dataframe=df,
            view=pie_view
        )

    @app.callback(
        Output("pie_graph", "figure", allow_duplicate=True),
        Input("vaccine_brand", "value"),
        prevent_initial_call=True)
    def vaccine_filter(vaccine):
        nonlocal pie_view
        if vaccine is None:
            filters_dict["Brand_first_vaccine"] = None
        else:
            filters_dict["Brand_first_vaccine"] = f'Brand_first_vaccine == "{vaccine}"'

        return calculate_graph(
            filters=filters_dict,
            original_dataframe=df,
            view=pie_view
        )

    @app.callback(
        Output("pie_graph", "figure", allow_duplicate=True),
        Input("pie_view", "value"),
        prevent_initial_call=True)
    def view_toggle(view):
        nonlocal pie_view
        if view is None:
            pie_view = None
        else:
            pie_view = view

        return calculate_graph(
            filters=filters_dict,
            original_dataframe=df,
            view=pie_view
        )

    # Run the app
    if __name__ == '__main__':
        app.run_server(debug=True)


def calculate_metadata(dataframe) -> dict:
    data = dict()

    vaccines = dataframe["Brand_first_vaccine"].unique().tolist()

    data[VACCINES] = vaccines + [None]

    return data


def calculate_graph(filters: dict, original_dataframe, view=None) -> px.pie:
    filter_string = ""

    if view == "LOCATION":
        names = "Department"
        filters["custom_filter"] = f'Final_state == "deceased"'
    else:
        names = "Final_state"
        filters.pop("custom_filter", None)

    for filter_element in list(filters.items()):
        if filter_element[1] is not None:
            if filter_string != "":
                filter_string += f" & {filter_element[1]}"
            else:
                filter_string = f"{filter_element[1]}"

    print(filter_string)
    filtered_df = original_dataframe.query(filter_string)
    return px.pie(filtered_df, title='Covid lethality', names=names)


if __name__ == "__main__":
    lethality_graph()
