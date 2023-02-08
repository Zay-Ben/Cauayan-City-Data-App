import streamlit as st
import plotly.express as px

st.header('Data Visualization')

if 'gdf_geojson' in st.session_state:
    
    gdf_geojson = st.session_state['gdf_geojson']
    gdf = st.session_state['gdf']
    df = st.session_state['df']
    dv = df
    
    columns = [column for column in df.columns if "Proportion" in column]
    
    proportions = st.multiselect(label = 'Which of the columns are you interested in?',
                                 options = proportions)
