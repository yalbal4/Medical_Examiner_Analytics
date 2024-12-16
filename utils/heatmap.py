from dash import Dash, html, dcc
import pandas as pd
import geopandas as gpd
from shapely.geometry import shape
import json
import folium
from folium.plugins import HeatMap

data = pd.read_csv("conneticut_wide_form.csv")
#data = data.head(10000)
data = data.dropna(subset='deathcitygeo')
data['geometry'] = data['deathcitygeo'].str.replace("'", '"')

# Ensure non-string values (e.g., NaN or floats) are handled
def safe_parse_location(value):
    if pd.isna(value) or not isinstance(value, str):
        return None  # Return None for invalid or missing values
    try:
        return shape(json.loads(value))  # Convert to Shapely geometry
    except json.JSONDecodeError:
        return None  # Return None for improperly formatted strings

# Apply the parsing function
data['geometry'] = data['geometry'].apply(safe_parse_location)
gdf = gpd.GeoDataFrame(data, geometry='geometry')
gdf.set_crs("EPSG:4326", inplace=True)
gdf['lon'] = gdf.geometry.x
gdf['lat'] = gdf.geometry.y

heat_data = gdf[['lat', 'lon']].values.tolist()

m = folium.Map(location=[gdf['lat'].mean(), gdf['lon'].mean()], zoom_start=10)

HeatMap(heat_data).add_to(m)

m.save('test_heat_map.html')

#load map html as string
with open('test_heat_map.html', 'r') as f:
    map_html = f.read()

app = Dash(__name__)

app.layout = html.Div([
    html.Iframe(children=map_html)
])

if __name__ == '__main__':
    app.run_server(debug=True)