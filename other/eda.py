import pandas as pd
import geopandas as gpd
import json
from shapely.geometry import shape

data_file_path = 'conneticut_wide_form.csv'
counties_geojson_file_path = 'CT_Counties.geojson'

data = pd.read_csv("conneticut_wide_form.csv")

print("injury county is null")
print(data['injurycounty'].isnull().sum())
print("death county is null")
print(data['deathcounty'].isnull().sum())

print("injury city geo is null")
print(data['injurycitygeo'].isnull().sum())
print("death city geo is null")
print(data[data['deathcitygeo'].isnull()])
print(data.iloc[8388]['deathcitygeo'])

print('both injury and death city geo null')
print(data[(data['injurycitygeo'].isnull()) & (data['deathcitygeo'].isnull())].shape[0])

print(f"geodata shape {data.shape[0]}")
data = data.dropna(subset='deathcitygeo')
print(f"geodata shape after dropna {data.shape[0]}")

# data preprocessing
data = data.dropna(subset='deathcitygeo')
data['deathcitygeo'] = data['deathcitygeo'].str.replace("'", '"')
data['geometry'] = data['deathcitygeo'].apply(lambda x: shape(json.loads(x)))
geodata = gpd.GeoDataFrame(data, geometry='geometry')

# data preprocessing
data = data.dropna(subset='deathcitygeo')
data['deathcitygeo'] = data['deathcitygeo'].str.replace("'", '"')
data['geometry'] = data['deathcitygeo'].apply(lambda x: shape(json.loads(x)))
death_geodata = gpd.GeoDataFrame(data, geometry='geometry', crs=4326)

# CT counties geodata
with open(counties_geojson_file_path, 'r') as f:
    counties_geojson = json.load(f)
counties_gdf = gpd.read_file(counties_geojson_file_path)

joined_gdf = gpd.sjoin(death_geodata, counties_gdf, how='left', predicate='within')
print(joined_gdf)