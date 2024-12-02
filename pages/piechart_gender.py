# Import packages
import dash
from dash import html, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import utils.charts as charts

dash.register_page(__name__, path="/pie", name="Pie Chart")

layout = html.Div(children=[
    dcc.Graph(id='graph-with-dropdown'),
    dcc.Dropdown(
        placeholder='Select year',
        value='All',
        id='year-dropdown'
    )
])

@callback(
    Output('year-dropdown', 'options'),
    Input('shared-df', 'data')
)
def populate_year_dropdown(shared_df):
    df = pd.read_json(shared_df)
    options = [str(year) for year in df['deceasedYear'].unique()] + ['All']
    return options

@callback(
    Output('graph-with-dropdown', 'figure'),
    [Input('year-dropdown', 'value'),
    Input('shared-df', 'data')]
)
def update_figure(selected_year, shared_df):
    df = pd.read_json(shared_df)
    
    if selected_year == "All":
        selected_year = None
    else:
        selected_year = int(selected_year)

    filters = {
        "deceasedYear": selected_year
    }

    fig = charts.pie_chart(df, 'gender', 'Overdoses by Sex', filters=filters)

    fig.update_layout(transition_duration=500)

    return fig