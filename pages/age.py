import dash
from dash import html, dcc, callback, Output, Input
import pandas as pd
import utils.charts as charts

dash.register_page(__name__, path="/age", name="Age Chart")

layout = html.Div(children=[
    dcc.Graph(id='age-chart'),
    dcc.Dropdown(
        placeholder='Select year, leave empty to select all',
        value=None,
        id='year-dropdown-age'
    ),
    dcc.Dropdown(
        placeholder='Select race, leave empty to select all',
        value=None,
        id='race-dropdown-age',
        multi=True
    ),
    dcc.Dropdown(
        ['Bar chart'],
        placeholder='Select chart type',
        value='Bar chart',
        id='chart-dropdown-age'
    )
])

@callback(
    Output('year-dropdown-age', 'options'),
    Input('shared-df', 'data')
)
def populate_year_dropdown(shared_df):
    df = pd.read_json(shared_df)
    options = [str(year) for year in df['deceasedYear'].unique()]
    return options

@callback(
    Output('race-dropdown-age', 'options'),
    Input('shared-df', 'data')
)
def populate_race_dropdown(shared_df):
    df = pd.read_json(shared_df)
    options = [str(race) for race in df['race'].unique()]
    return options

@callback(
    Output('age-chart', 'figure'),
    [Input('chart-dropdown-age', 'value'),
     Input('year-dropdown-age', 'value'),
     Input('race-dropdown-age', 'value'),
     Input('shared-df', 'data')]
)
def update_figure(selected_chart, selected_year, selected_races, shared_df):
    df = pd.read_json(shared_df)
    
    if selected_year is not None:
        selected_year = int(selected_year)

    if selected_races is None or len(selected_races) == 0:
        selected_races = None

    filters = {
        "deceasedYear": selected_year,
        "race": selected_races
    }

    fig = charts.build_chart(selected_chart, df, 'age', 'Overdoses by Age', filters=filters)

    return fig