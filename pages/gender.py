import dash
from dash import html, dcc, callback, Output, Input
import pandas as pd
import utils.charts as charts

dash.register_page(__name__, path="/pie_gender", name=" Gender Pie Chart")

layout = html.Div(children=[
    dcc.Graph(id='gender-chart'),
    dcc.Dropdown(
        placeholder='Select year, leave empty to select all',
        value=None,
        id='year-dropdown-gender'
    ),
    dcc.Dropdown(
        placeholder='Select race, leave empty to select all',
        value=None,
        id='race-dropdown-gender',
        multi=True
    ),
    dcc.Dropdown(
        ['Pie chart', 'Bar chart'],
        placeholder='Select chart type',
        value=None,
        id='chart-dropdown-gender'
    )
])

@callback(
    Output('year-dropdown-gender', 'options'),
    Input('shared-df', 'data')
)
def populate_year_dropdown(shared_df):
    df = pd.read_json(shared_df)
    options = [str(year) for year in df['deceasedYear'].unique()]
    return options

@callback(
    Output('race-dropdown-gender', 'options'),
    Input('shared-df', 'data')
)
def populate_race_dropdown(shared_df):
    df = pd.read_json(shared_df)
    options = [str(race) for race in df['race'].unique()]
    return options

@callback(
    Output('gender-chart', 'figure'),
    [Input('chart-dropdown-gender', 'value'),
     Input('year-dropdown-gender', 'value'),
     Input('race-dropdown-gender', 'value'),
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

    fig = charts.pie_chart(df, 'gender', 'Overdoses by Sex', filters=filters)

    fig.update_layout(transition_duration=500)

    return fig