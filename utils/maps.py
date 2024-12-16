from dash.dependencies import Input, Output
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import geopandas as gpd
import json
from shapely.geometry import shape

data_file_path = 'conneticut_wide_form.csv'
counties_geojson_file_path = 'CT_Counties.geojson'
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

deaths_by_county = group_deaths_by_county_and_year(joined_gdf)

fig = create_choropleth_fig(deaths_by_county)

# Update layout for map visualization
fig.update_geos(fitbounds="locations", visible=True)
fig.update_layout(title="Medical Examiner Deaths by County")

# fig.show()

app = Dash()

app.layout = html.Div([
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=True)