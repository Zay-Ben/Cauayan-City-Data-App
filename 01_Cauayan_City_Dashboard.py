import pandas as pd
import json
import geopandas as gpd
import streamlit as st

st.title('Cauayan City Dashboard')

st.header('Data Table')

#

data = pd.read_csv('output/data.csv')

data['Column'] = data['Column'].apply(lambda x: x.split('+'))

with open('output/ssot.geojson') as f:
    gdf_geojson = json.load(f)
    
gdf = gpd.GeoDataFrame.from_features(gdf_geojson)

# Data

st.subheader('Data')

x = st.multiselect(label = '',
                   options = set(data['Data']),
                   default = set(data['Data']),
                   label_visibility = 'collapsed')

# Sheet

st.subheader('Sheet')

sheet = data[data['Data'].isin(x)]['Sheet']

y_options = st.radio(label = 'View all sheets:',
                     options = ['Yes', 'No'])

if y_options == 'Yes':
    y_default = sheet
else:
    y_default = None
    
y = st.multiselect(label = '',
                   options = sheet,
                   default = y_default,
                   label_visibility = 'collapsed')

# Column

st.subheader('Column')

column = [j for i in data[data['Data'].isin(x)][data['Sheet'].isin(y)]['Column'] for j in i]

#

options = st.radio(label = 'View all columns:',
                   options = ['With male and female', 'Without male and female', 'With male only', 'With female only'])

if options == 'With male and female':
    pass
elif options == 'Without male and female':
    column = [i for i in column if 'Male' not in i if 'Female' not in i]
elif options == 'With male only':
    column = [i for i in column if 'Male' in i]
else:
    column = [i for i in column if 'Female' in i]
    
#

z_options = st.radio(label = 'View all columns:',
                     options = ['Yes', 'No'])

if z_options == 'Yes':
    z_default = column
else:
    z_default = None
    
z = st.multiselect(label = '',
                   options = column,
                   default = z_default,
                   label_visibility = 'collapsed')

#

if z is not None:
    df = gdf[['geometry', 'Barangay'] + z]
    
#

st.dataframe(df.drop(columns = 'geometry').set_index(keys = 'Barangay'))

#

db_options = st.radio(label = 'Download data as:',
                      options = ['ssot.csv (without location coordinates)', 'ssot.geojson (with location coordinates)'])

if db_options == 'ssot.csv (without location coordinates)':
    df_label = 'ssot.csv'
    df_data = df.drop(columns = 'geometry').to_csv(index = False)
    df_file_name = 'ssot.csv'
else:
    df_label = 'ssot.geojson'
    df_data = df.to_json()
    df_file_name = 'ssot.geojson'
    
st.download_button(label = df_label,
                   data = df_data,
                   file_name = df_file_name)

#

st.session_state['gdf_geojson'] = gdf_geojson
st.session_state['gdf'] = gdf
st.session_state['df'] = df
