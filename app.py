import streamlit as st
import api

st.set_page_config(page_title="Getaway Carbs")
st.title("Getaway Carbs")

posts = api.get_posts()

for post in posts:
    box = st.container(border=True)
    with box:
        st.title(post["restaurant"])
        st.write(f'**Organizer:** {post["author"]["username"]}')
        st.write(f'**Order Type:** {post["order"]}')
        st.write(f'**Leaving at:** {post["departure"][11:16]}')
        st.write(f'**Additional Notes:** {post["notes"]}')


