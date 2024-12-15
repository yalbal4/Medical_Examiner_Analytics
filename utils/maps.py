import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash import Dash, html
import plotly.express as px
import pandas as pd
import geopandas as gpd
import json
from shapely.geometry import shape

data = pd.read_csv("conneticut_wide_form.csv")

# data preprocessing
data = data.dropna(subset='deathcitygeo')
data['deathcitygeo'] = data['deathcitygeo'].str.replace("'", '"')
data['geometry'] = data['deathcitygeo'].apply(lambda x: shape(json.loads(x)))
geodata = gpd.GeoDataFrame(data, geometry='geometry')

# data["deathcitygeo"] = data["deathcitygeo"].astype(str)
# data[['longitude', 'latitude']] = data["deathcitygeo"].str.extract(r'\[([\d\.-]+),\s*([\d\.-]+)\]')
# data['latitude'] = pd.to_numeric(data['latitude'])
# data['longitude'] = pd.to_numeric(data['longitude'])

# data_head100 = data.head(100)

# geodicts = [dict(lat=row['latitude'], lon=row['longitude']) for _, row in data_head100.iterrows()]
# data_geojson = dlx.dicts_to_geojson(geodicts)

with open('CT_Counties.geojson', 'r') as f:
    counties_geojson = json.load(f)

counties_gdf = gpd.read_file('CT_Counties.geojson')

test_data = counties_gdf[['OBJECTID']]
test_data['value'] = range(len(counties_gdf))
test_data['value'] += 10

joined_gdf = gpd.sjoin(geodata, counties_gdf, how='left', predicate='within')

deaths_by_county = joined_gdf.groupby('OBJECTID').size()
deaths_by_county = deaths_by_county.reset_index()
print(deaths_by_county)

fig = px.choropleth(
    deaths_by_county,
    geojson=counties_geojson,
    locations='OBJECTID',
    color=0,
    scope='usa'
)

fig.show()
# app = Dash()
# app.layout = html.Div([
#     dl.Map(children=[
#         dl.TileLayer(),
#         dl.GeoJSON(data=data_geojson)
#     ], style={'height': '50vh'}, center=[data_head100['latitude'].median(), data_head100['longitude'].median()], zoom=6)
# ])

# if __name__ == '__main__':
#     app.run_server(debug=True)