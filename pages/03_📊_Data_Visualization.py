import streamlit as st
import plotly.express as px

st.header('Data Visualization')

if 'gdf_geojson' in st.session_state:
    
    gdf_geojson = st.session_state['gdf_geojson']
    gdf = st.session_state['gdf']
    df = st.session_state['df']
    dv = df
    
    i_options = list(df.columns[2:])
    
    if 'Total no. of Households' in i_options:
        i_options.remove('Total no. of Households')
    if 'Total no. of Population' in i_options:
        i_options.remove('Total no. of Population')
        
    i = st.selectbox(label = 'Which of the columns are you interested in?',
                     options = df.columns[2:])

    if i is not None:

        lst = [i, 'As % of Total no. of Households', 'As % of Total no. of Population', 'As % of ' + i]

        j = st.radio(label = 'How would you like to visualize the data?',
                     options = lst,
                     index = 0)

        if j == lst[0]:
            dv_hd = ['Barangay', i]
            dv_ht = '<br>'.join(['<b>%{customdata[0]}</b>',
                                 i + ': %{customdata[1]}'])
        elif j == lst[1]:
            dv['Total no. of Households'] = gdf['Total no. of Households']
            dv[j] = round(df[i] / dv['Total no. of Households'] * 100, 2)
            dv_hd = ['Barangay', i, 'Total no. of Households', j]
            dv_ht = '<br>'.join(['<b>%{customdata[0]}</b>',
                                 i + ': %{customdata[1]}',
                                 'Total no. of Households: %{customdata[2]}',
                                 j + ': %{customdata[3]}'])
        elif j == lst[2]:
            dv['Total no. of Population'] = gdf['Total no. of Population']
            dv[j] = round(df[i] / dv['Total no. of Population'] * 100, 2)
            dv_hd = ['Barangay', i, 'Total no. of Population', j]
            dv_ht = '<br>'.join(['<b>%{customdata[0]}</b>',
                                 i + ': %{customdata[1]}',
                                 'Total no. of Households: %{customdata[2]}',
                                 j + ': %{customdata[3]}'])
        else:
            dv[j] = round(df[i] / sum(df[i]) * 100, 2)
            dv_hd = ['Barangay', i, j]
            dv_ht = '<br>'.join(['<b>%{customdata[0]}</b>',
                                 i + ': %{customdata[1]}',
                                 j + ': %{customdata[2]}'])

        # Choropleth Map

        st.subheader('Choropleth Map')

        cm = px.choropleth(data_frame = dv,
                           locations = 'Barangay',
                           geojson = gdf_geojson,
                           featureidkey = 'properties.Barangay',
                           color = j,
                           hover_data = dv_hd,
                           center = {'lat' : dv.centroid.x.mean(), 'lon' : dv.centroid.y.mean()},
                           fitbounds = 'locations',
                           basemap_visible = False,
                           width = 800,
                           height = 400)

        cm.update_layout(margin = {'r' : 0, 't' : 0, 'l' : 0, 'b' : 0})

        cm.update_traces(hovertemplate = dv_ht)

        st.plotly_chart(cm)

        # Bar Chart

        st.subheader('Bar Chart')

        dv_10 = dv.sort_values(by = j, ascending = False).head(10)

        bc = px.bar(data_frame = dv_10,
                    x = 'Barangay',
                    y = j,
                    color = j,
                    hover_data = ['Barangay', j],
                    text = j,
                    width = 800,
                    height = 400)

        bc.update_traces(hovertemplate = '<br>'.join(['<b>%{x}</b>',
                                                      j + ': %{y}']))

        st.plotly_chart(bc)

        #

        st.subheader('How it is computed?')

        st.code(body = '''
df['As % of Total no. of Households'] = round(df[Column] / df['Total no. of Households * 100, 2)
df['As % of Total no. of Population'] = round(df[Column] / Total no. of Population * 100, 2)
df['As % of ' + Column] = round(df[Column] / sum(df[Column]) * 100, 2)
        ''',
                language = 'python')
        
