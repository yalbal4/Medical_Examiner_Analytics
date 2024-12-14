import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash import Dash, html
import pandas as pd
import json

# app = Dash()
# app.layout = html.Div([
#     dl.Map([
#         dl.TileLayer(),
#         # From in-memory geojson. All markers at same point forces spiderfy at any zoom level.
#         dl.GeoJSON(data=dlx.dicts_to_geojson([dict(lat=-37.8, lon=175.5)] * 50), cluster=True),
#     ], center=(-37.75, 175.4), zoom=11, style={'height': '50vh'}),
# ])

# if __name__ == '__main__':
#     app.run_server()

data = pd.read_csv("conneticut_wide_form.csv")
data["deathcitygeo"] = data["deathcitygeo"].astype(str)
data[['longitude', 'latitude']] = data["deathcitygeo"].str.extract(r'\[([\d\.-]+),\s*([\d\.-]+)\]')
data['latitude'] = pd.to_numeric(data['latitude'])
data['longitude'] = pd.to_numeric(data['longitude'])

data_head100 = data.head(100)


geodicts = [dict(lat=row['latitude'], lon=row['longitude']) for _, row in data_head100.iterrows()]
geojson = dlx.dicts_to_geojson(geodicts)
# geojson = dlx.dicts_to_geojson([dict(lat=41.57, lon=-72.38)])
# print(geojson)
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