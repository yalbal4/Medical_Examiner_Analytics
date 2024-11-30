# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

# Incorporate data
df = pd.read_csv('conneticut_wide_form.csv')

by_gender_df = df.groupby('sex').size()
gender_fig = px.pie(by_gender_df, values=by_gender_df.values, names=by_gender_df.index, title='Overdoses by Sex')

# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='by-gender-graph',
        figure=gender_fig
    )
])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
