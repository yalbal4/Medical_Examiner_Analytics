# Import packages
import dash
from dash import html, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

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
def populate_dropdown(shared_df):
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
        filtered_df = df
    else:
        filtered_df = df[df['deceasedYear'] == int(selected_year)]
    
    by_gender_df = filtered_df.groupby('gender').size()

    fig = px.pie(by_gender_df, values=by_gender_df.values, names=by_gender_df.index, title='Overdoses by Sex')

    fig.update_layout(transition_duration=500)

    return fig