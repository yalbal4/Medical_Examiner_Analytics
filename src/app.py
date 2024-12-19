from dash.dependencies import Input, Output
from dash import Dash, html, dcc, callback, Input, Output, ctx
import plotly.express as px
import pandas as pd
import geopandas as gpd
import json
from shapely.geometry import shape
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
data_folder = project_root / 'data'

data_file_path = data_folder / 'conneticut_wide_form.csv'
counties_geojson_file_path = data_folder / 'CT_Counties.geojson'
geolocation_column_name = 'injurycitygeo'

data = pd.read_csv(data_file_path)

# data preprocessing
data = data.dropna(subset=geolocation_column_name)
data[geolocation_column_name] = data[geolocation_column_name].str.replace("'", '"')
data['geometry'] = data[geolocation_column_name].apply(lambda x: shape(json.loads(x)))
death_geodata = gpd.GeoDataFrame(data, geometry='geometry', crs=4326)

# CT counties geodata
with open(counties_geojson_file_path, 'r') as f:
    counties_geojson = json.load(f)
counties_gdf = gpd.read_file(counties_geojson_file_path)

joined_gdf = gpd.sjoin(death_geodata, counties_gdf, how='left', predicate='within')

def group_deaths_by_county_and_year(df, counties_gdf):
    df_copy = df.copy()
    df_copy = df_copy.groupby(['OBJECTID', 'death_year']).size()
    df_copy = df_copy.reset_index()
    # regain county data lost from the groupby
    df_copy = pd.merge(df_copy, counties_gdf, on='OBJECTID', how='left')
    df_copy = df_copy.rename(columns={0: 'death_count'})
    return df_copy

def create_choropleth_fig(df, locations_geojson):
    fig = px.choropleth(
        df,
        geojson=locations_geojson,
        locations='OBJECTID',
        color='death_count',
        scope='usa',
        hover_name='COUNTY',
        hover_data={
            "OBJECTID": False,
            "death_count": False,
            "Death Count": df['death_count']},
        animation_frame='death_year'
    )
    return fig

def create_county_time_series(df, county_id=None, county_name=None):
    if county_id is not None:
        df_copy = df.copy()
        df_copy = df[df['CNTY_NO'] == county_id]
    else:
        df_copy = df.copy()
        df_copy = df_copy.drop(['geometry'], axis=1)
        df_copy = df_copy.groupby('death_year').sum()
        df_copy = df_copy.reset_index()
        
    if county_name is not None:
        title = county_name + ' County Deaths Over Time'
    else:
        title = 'Connecticut Deaths Over Time'

    fig = px.scatter(df_copy, x='death_year', y='death_count', title=title)
    fig.update_traces(mode='lines+markers')
    fig.update_xaxes(showgrid=False)
    return fig

deaths_by_county = group_deaths_by_county_and_year(joined_gdf, counties_gdf)
# print(f"deaths_by_county {deaths_by_county}")

map_fig = create_choropleth_fig(deaths_by_county, counties_geojson)
# Update layout for map visualization
map_fig.update_geos(fitbounds="locations", visible=True)
map_fig.update_layout(title="Medical Examiner Deaths by County")

time_series_fig = create_county_time_series(deaths_by_county, None, None)

app = Dash(__name__)
server = app.server

app.layout = html.Div([
    dcc.Graph(id='county-map', figure=map_fig),
    html.Button('Unselect County', id='clear-county-button'),
    dcc.Graph(id='county-time-series', figure=time_series_fig)
])

# REMOVE when finalized
# @callback(
#     Output(component_id='test-div', component_property='children'),
#     Input(component_id='county-map', component_property='hoverData')
# )
# def update_div(map_hover_data):
#     if map_hover_data is None:
#         return None
#     county_id = map_hover_data['points'][0]['location']
#     county_name = map_hover_data['points'][0]['hovertext']
#     create_county_time_series(deaths_by_county, county_id, county_name)
#     return county_id

@callback(
    Output(component_id='county-time-series', component_property='figure'),
    Input(component_id='county-map', component_property='clickData'),
    Input(component_id='clear-county-button', component_property='n_clicks')
)
def update_time_series(map_click_data, button_click):
    if 'clear-county-button' == ctx.triggered_id:
        return create_county_time_series(deaths_by_county, None, None)
    
    if map_click_data is None:
        return create_county_time_series(deaths_by_county, None, None)

    county_id = map_click_data['points'][0]['location']
    county_name = map_click_data['points'][0]['hovertext']
    fig = create_county_time_series(deaths_by_county, county_id, county_name)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)