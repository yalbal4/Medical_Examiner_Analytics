from dash.dependencies import Input, Output
from dash import Dash, html, dcc, callback, Input, Output
import plotly.express as px
import pandas as pd
import geopandas as gpd
import json
from shapely.geometry import shape

data_file_path = 'data\conneticut_wide_form.csv'
counties_geojson_file_path = 'data\CT_Counties.geojson'
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


def group_deaths_by_county_and_year(df):
    df = joined_gdf.groupby(['OBJECTID', 'death_year']).size()
    df = df.reset_index()
    df = pd.merge(df, counties_gdf, on='OBJECTID', how='left')
    df = df.rename(columns={0: 'death_count'})
    return df

def create_choropleth_fig(df):
    fig = px.choropleth(
        df,
        geojson=counties_geojson,
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

deaths_by_county = group_deaths_by_county_and_year(joined_gdf)
# print(f"deaths_by_county {deaths_by_county}")

map_fig = create_choropleth_fig(deaths_by_county)
# Update layout for map visualization
map_fig.update_geos(fitbounds="locations", visible=True)
map_fig.update_layout(title="Medical Examiner Deaths by County")

time_series_fig = create_county_time_series(deaths_by_county, None, None)

app = Dash()

app.layout = html.Div([
    dcc.Graph(id='county-map', figure=map_fig),
    dcc.Graph(id='county-time-series', figure=time_series_fig),
    html.Div(id='test-div', children='helo')
])

@callback(
    Output(component_id='test-div', component_property='children'),
    Input(component_id='county-map', component_property='hoverData')
)
def update_div(map_hover_data):
    if map_hover_data is None:
        return None
    county_id = map_hover_data['points'][0]['location']
    county_name = map_hover_data['points'][0]['hovertext']
    create_county_time_series(deaths_by_county, county_id, county_name)
    return county_id

@callback(
    Output(component_id='county-time-series', component_property='figure'),
    Input(component_id='county-map', component_property='hoverData')
)
def update_time_series(map_hover_data):
    if map_hover_data is None:
        return create_county_time_series(deaths_by_county, None, None)

    county_id = map_hover_data['points'][0]['location']
    county_name = map_hover_data['points'][0]['hovertext']
    fig = create_county_time_series(deaths_by_county, county_id, county_name)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)