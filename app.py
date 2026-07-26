import streamlit as st
import api
from datetime import datetime, time

st.set_page_config(page_title="Getaway Carbs")
st.title("Getaway Carbs")
st.space("large")

create, plans = st.tabs(["Create a Plan", "View Plans"]) 

with create:
    st.header("Create a New Plan")
    restaurant = st.text_input("Restaurant Name")
    order_type = st.selectbox("Order Type", ["Dine In", "Takeout", "Pickup"])
    departure_time = st.time_input("Departure Time", step=300, value="12:00")
    notes = st.text_area("Additional Notes (Optional)")
    username = st.text_input("Your Name")

    if st.button("Create Plan"):
        if not restaurant or not order_type or not departure_time or not username:
            st.error("Please fill in all required fields.")
        else:
            post_data = {
                "restaurant": restaurant,
                "order": order_type,
                "departure": departure_time.strftime("%H:%M"),
                "notes": notes,
                "user_id": api.get_id(username)
            }
            response = api.create_post(post_data)
            if response.status_code == 201:
                st.success("Plan created successfully!")
            else:
                st.error(f"Error creating plan: {response.json().get('detail', 'Unknown error')}")

with plans:
    posts = api.get_posts()
    def parse_departure(post):
        departure = post.get("departure", "")
        if departure.endswith("Z"):
            departure = departure[:-1] + "+00:00"
        try:
            return datetime.fromisoformat(departure)
        except ValueError:
            return datetime.min
    for post in sorted(posts, key=parse_departure):
        box = st.container(border=True)
        with box:
            st.title(post["restaurant"])
            st.write(f'**Organizer:** {post["author"]["username"]}')
            st.write(f'**Order Type:** {post["order"]}')
            st.write(f'**Leaving at:** {post["departure"][11:16]}')
            st.write(f'**Additional Notes:** {post["notes"]}')
            st.write(f'**Participants:** {", ".join([p["user"]["username"] for p in post["participants"]])}')
            with st.form(f"join_form_{post['id']}"):
                name = st.text_input("Your Name", key=f"name_{post['id']}")
                submitted = st.form_submit_button("Join Plan")
                if submitted:
                    if not name:
                        st.error("Please enter your name to join")
                    else:
                        user_id = api.get_id(name)
                        if user_id is None:
                            st.error("User not found. Please create a plan first.")
                        else:
                            join_response = api.join_plan(post["id"], user_id)
                            if join_response.status_code == 201:
                                st.rerun()
                            else:
                                st.error(f"Error joining plan: {join_response.json().get('detail', 'Unknown error')}")


