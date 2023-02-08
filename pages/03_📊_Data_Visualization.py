import streamlit as st
import plotly.express as px

st.header('Data Visualization')

if 'gdf_geojson' in st.session_state:
    
    gdf_geojson = st.session_state['gdf_geojson']
    gdf = st.session_state['gdf']
    df = st.session_state['df']
    dv = df
    
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
            dv[j] = round(df[i] / sum(dv['Total no. of Households']) * 100, 2)
            dv_hd = ['Barangay', i, 'Total no. of Households', j]
            dv_ht = '<br>'.join(['<b>%{customdata[0]}</b>',
                                 i + ': %{customdata[1]}',
                                 'Total no. of Households: %{customdata[2]}',
                                 j + ': %{customdata[3]}'])
        elif j == lst[2]:
            dv['Total no. of Population'] = gdf['Total no. of Population']
            dv[j] = round(df[i] / sum(dv['Total no. of Population']) * 100, 2)
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
            
        sort = st.radio(label = 'How would you like to sort the data?',
                        options = ['Sort in ascending order', 'Sort in descending order'],
                        index = 1)
        
        if sort == 'Sort in ascending order':
            dv_10 = dv.sort_values(by = j, ascending = False).tail(10)
            k = 'lowest'
        else:
            dv_10 = dv.sort_values(by = j, ascending = False).head(10)
            k = 'highest'
            
        st.subheader('Which barangay has the {0} {1}?'.format(k, j))
        
        # Choropleth Map
        
        cm = px.choropleth(data_frame = dv,
                           locations = 'Barangay',
                           geojson = gdf_geojson,
                           featureidkey = 'properties.Barangay',
                           color = j,
                           hover_data = dv_hd,
                           color_continuous_scale = px.colors.sequential.Plasma,
                           center = {'lat' : dv.centroid.x.mean(), 'lon' : dv.centroid.y.mean()},
                           fitbounds = 'locations',
                           basemap_visible = False,
                           width = 800,
                           height = 400)

        cm.update_layout(margin = {'r' : 0, 't' : 0, 'l' : 0, 'b' : 0})

        cm.update_traces(hovertemplate = dv_ht)

        st.plotly_chart(cm)
        
        # Bar Chart
        
        bc = px.bar(data_frame = dv_10,
                    x = 'Barangay',
                    y = j,
                    color = j,
                    hover_data = ['Barangay', j],
                    text = j,
                    color_continuous_scale = px.colors.sequential.Plasma,
                    width = 800,
                    height = 400)

        bc.update_traces(hovertemplate = '<br>'.join(['<b>%{x}</b>',
                                                      j + ': %{y}']))

        st.plotly_chart(bc)

        #

        st.subheader('How it\'s computed?')

        st.code(body = '''
df['As % of Total no. of Households'] = round(df[Column] / sum(df['Total no. of Households']) * 100, 2)
df['As % of Total no. of Population'] = round(df[Column] / sum(df['Total no. of Population']) * 100, 2)
df['As % of ' + Column] = round(df[Column] / sum(df[Column]) * 100, 2)
        ''',
                language = 'python')
        
