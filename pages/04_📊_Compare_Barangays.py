import streamlit as st
import plotly.express as px

st.header('Compare Barangays')

if 'gdf_geojson' in st.session_state:
    
    gdf_geojson = st.session_state['gdf_geojson']
    gdf = st.session_state['gdf']
    df = st.session_state['df']
    dv = df.set_index(keys = "Barangay")
    
    columns = [column for column in df.columns if "Proportion" in column]
    
    proportions = st.multiselect(label = 'Which of the columns are you interested in?', options = columns)
    
    col1, col2 = st.columns(2)
    
    with col1:
        barangay1 = st.selectbox(label = 'Select Barangay 1:', options = df['Barangay'])
        dv1 = dv.loc[barangay1][proportions]
        st.plotly_chart(px.bar_polar(data_frame = dv1,
                                     r = dv1.values,
                                     theta = dv1.index,
                                     color_continuous_scale = px.colors.sequential.Plasma,
                                     width = 300,
                                     height = 300))
        
    with col2:
        barangay2 = st.selectbox(label = 'Select Barangay 2:', options = df['Barangay'])
        dv2 = dv.loc[barangay1][proportions]
        st.plotly_chart(px.bar_polar(data_frame = dv2,
                                     r = dv2.values,
                                     theta = dv2.index,
                                     color_continuous_scale = px.colors.sequential.Plasma,
                                     width = 300,
                                     height = 300))
        
