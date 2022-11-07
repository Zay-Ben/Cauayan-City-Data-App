import streamlit as st

st.title('Cauayan City Dashboard')

st.caption('Made by Ronald Benz M. Zhang')

st.markdown('This app allows users to access the data of the Cauayan City for academic and research purposes.')

video_file = open('Cauayan City Dashboard Demo.webm', 'rb')

video_bytes = video_file.read()

st.video(video_bytes)
