# Import packages
import dash
from dash import Dash, html, dcc
import pandas as pd
from utils.fhir_utils import fetch_patient_data, handle_deceased_datetime_add_helper_columns
import dash_bootstrap_components as dbc

USE_FHIR = False
ORIGINAL_DATE_COLUMN_NAME = 'date'
ORIGINAL_GENDER_COLUMN_NAME = 'sex'
ORIGINAL_AGE_COLUMN_NAME = 'age'
ORIGINAL_RACE_COLUMN_NAME = 'race'

# Incorporate data
if USE_FHIR:
    df = fetch_patient_data(count=5000000) # assumes the server url is http://localhost:8080/fhir
    df = handle_deceased_datetime_add_helper_columns(df)
else:
    df = pd.read_csv('conneticut_wide_form.csv')
    df.rename(columns={ORIGINAL_DATE_COLUMN_NAME:'deceasedDateTime',
                       ORIGINAL_GENDER_COLUMN_NAME: 'gender',
                       ORIGINAL_AGE_COLUMN_NAME: 'age',
                       ORIGINAL_RACE_COLUMN_NAME: 'race'},
              inplace=True)
    df = handle_deceased_datetime_add_helper_columns(df)

app = Dash(__name__, use_pages=True)
app.title = "Multi-Page Dash App"

app.layout = html.Div([
    dcc.Store(id="shared-df", data=df.to_json()),
    html.H1("Heading 1"),
    dbc.Nav([
        dbc.NavLink("Gender Pie Chart", href="/pie_gender", active="exact"), dash.html.Br(),
        dbc.NavLink("Gender Bar Chart", href="/bar_gender", active="exact"), dash.html.Br(),
    ], pills=True),
    dash.page_container
])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
