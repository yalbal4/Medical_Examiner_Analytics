# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
from fhir_utils import fetch_patient_data, handle_deceased_datetime_add_helper_columns
# import dash_bootstrap_components as dbc

# Incorporate data
df = fetch_patient_data(count=5000000) # assumes the server url is http://localhost:8080/fhir
df = handle_deceased_datetime_add_helper_columns(df)

app = Dash(__name__)

app.layout = html.Div(children=[
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        df['deceasedYear'].min(),
        df['deceasedYear'].max(),
        step=None,
        value=df['deceasedYear'].min(),
        marks={str(year): str(year) for year in df['deceasedYear'].unique()},
        id='year-slider'
    )
])

@callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value'))
def update_figure(selected_year):
    filtered_df = df[df['deceasedYear'] == selected_year]
    by_gender_df = filtered_df.groupby('gender').size()

    fig = px.pie(by_gender_df, values=by_gender_df.values, names=by_gender_df.index, title='Overdoses by Sex')

    fig.update_layout(transition_duration=500)

    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
