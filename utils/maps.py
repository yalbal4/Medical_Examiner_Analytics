import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash import Dash, html
import pandas as pd
import json

data = pd.read_csv("conneticut_wide_form.csv")
data["deathcitygeo"] = data["deathcitygeo"].astype(str)
data[['longitude', 'latitude']] = data["deathcitygeo"].str.extract(r'\[([\d\.-]+),\s*([\d\.-]+)\]')
data['latitude'] = pd.to_numeric(data['latitude'])
data['longitude'] = pd.to_numeric(data['longitude'])

data_head100 = data.head(100)

geodicts = [dict(lat=row['latitude'], lon=row['longitude']) for _, row in data_head100.iterrows()]
geojson = dlx.dicts_to_geojson(geodicts)
# geojson = dlx.dicts_to_geojson([dict(lat=41.57, lon=-72.38)])
print(geojson)
# print(data.head())

app = Dash()
app.layout = html.Div([
    dl.Map(children=[
        dl.TileLayer(),
        dl.GeoJSON(data=geojson)
    ], style={'height': '50vh'}, center=[data_head100['latitude'].median(), data_head100['longitude'].median()], zoom=6)
])

if __name__ == '__main__':
    app.run_server(debug=True)