import streamlit as st
import api

st.set_page_config(page_title="Getaway Carbs", layout="wide")
st.title("Getaway Carbs")

st.write(api.get_posts())
