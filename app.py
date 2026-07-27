import streamlit as st
import api
from datetime import datetime, time
from zoneinfo import ZoneInfo

CENTRAL = ZoneInfo("America/Chicago")

if "user_id" not in st.session_state:
    st.title("Welcome to Getaway Carbs")

    with st.form("user_form"):
        username = st.text_input("Enter your name")
        submitted = st.form_submit_button("Continue")

        if submitted:
            ident = api.get_id(username)
            if ident:
                st.session_state["user_id"] = ident
                st.session_state["username"] = username
                st.rerun()
            else:
                response = api.create_user(username)

                if response.status_code == 201:
                    user = response.json()

                    st.session_state["user_id"] = user["id"]
                    st.session_state["username"] = user["username"]

                    st.rerun()
                else:
                    st.error(response.json().get("detail", "Something went wrong"))

    st.stop()

st.set_page_config(page_title="Getaway Carbs")
st.title("Getaway Carbs")
st.space("large")

create, plans, mine = st.tabs(["Create a Plan", "View Plans", "My Plans"]) 

with create:
    st.header("Create a New Plan")
    restaurant = st.text_input("Restaurant Name")
    order_type = st.selectbox("Order Type", ["Dine In", "Takeout", "Pickup"])
    departure_time = st.time_input("Departure Time", step=300, value="12:00")
    notes = st.text_area("Additional Notes (Optional)")

    if st.button("Create Plan"):
        if not restaurant or not order_type or not departure_time:
            st.error("Please fill in all required fields.")
        else:
            post_data = {
                "restaurant": restaurant,
                "order": order_type,
                "departure": departure_time.strftime("%H:%M"),
                "notes": notes,
                "user_id": st.session_state["user_id"]
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
            parsed = datetime.fromisoformat(departure)
            if parsed.tzinfo is None:
                return parsed.replace(tzinfo=CENTRAL)
            return parsed.astimezone(CENTRAL)
        except ValueError:
            return datetime.min.replace(tzinfo=CENTRAL)

    now_central = datetime.now(CENTRAL)
    upcoming_posts = [post for post in posts if parse_departure(post) >= now_central]

    for post in sorted(upcoming_posts, key=parse_departure):
        box = st.container(border=True)
        with box:
            st.title(post["restaurant"])
            st.write(f'**Organizer:** {post["author"]["username"]}')
            st.write(f'**Order Type:** {post["order"]}')
            st.write(f'**Leaving at:** {post["departure"][11:16]}')
            st.write(f'**Additional Notes:** {post["notes"]}')
            st.write(f'**Participants:** {", ".join([p["user"]["username"] for p in post["participants"]])}')
            if st.button("Join Plan", key=f"join_{post['id']}"):
                user_id = st.session_state["user_id"]
                response = api.join_plan(post["id"], user_id)
                if response.status_code == 201:
                    st.success("Successfully joined the plan!")
                    st.rerun()
                else:
                    st.error(f"Error joining plan: {response.json().get('detail', 'Unknown error')}")

with mine:
    posts = api.get_user_posts(st.session_state["user_id"])

    def parse_departure(post):
        departure = post.get("departure", "")
        if departure.endswith("Z"):
            departure = departure[:-1] + "+00:00"
        try:
            parsed = datetime.fromisoformat(departure)
            if parsed.tzinfo is None:
                return parsed.replace(tzinfo=CENTRAL)
            return parsed.astimezone(CENTRAL)
        except ValueError:
            return datetime.min.replace(tzinfo=CENTRAL)

    now_central = datetime.now(CENTRAL)
    upcoming_posts = [post for post in posts if parse_departure(post) >= now_central]

    for post in sorted(upcoming_posts, key=parse_departure):
        box = st.container(border=True)
        with box:
            st.title(post["restaurant"])
            st.write(f'**Order Type:** {post["order"]}')
            st.write(f'**Leaving at:** {post["departure"][11:16]}')
            st.write(f'**Additional Notes:** {post["notes"]}')
            st.write(f'**Participants:** {", ".join([p["user"]["username"] for p in post["participants"]])}')
            if st.button("Delete Plan", key=f"delete_{post['id']}"):
                response = api.delete_post(post["id"])
                if response.status_code == 204:
                    st.success("Plan deleted successfully!")
                    st.rerun()
                else:
                    st.error(f"Error deleting plan: {response.json().get('detail', 'Unknown error')}")


