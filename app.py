import streamlit as st
import api

st.set_page_config(page_title="Getaway Carbs")
st.title("Getaway Carbs")

posts = api.get_posts()

for post in posts:
    box = st.container(border=True)
    with box:
        st.title(post["author"]["username"])
        st.write(post["restaurant"])
        st.write(post["order"])
        st.write(f'Leaving at {post["departure"]}')
        st.write(post["notes"])


