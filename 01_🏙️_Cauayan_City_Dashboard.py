import streamlit as st

st.set_page_config(page_title = 'Cauayan City Dashboard')

st.title('Cauayan City Dashboard')

st.caption('Made by Ronald Benz M. Zhang')

st.text('This app allows users to access the data of the Cauayan City for academic and research purposes.')

video_file = open('Cauayan City Dashboard.webm', 'rb')

video_bytes = video_file.read()

st.video(video_bytes)
