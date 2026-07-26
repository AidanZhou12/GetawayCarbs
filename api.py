import requests
import json

url = "http://localhost:8000/api/"

def get_posts():
    response = requests.get(url + "posts")
    if response.status_code == 200:
        posts = response.json()
        return posts
    else:
        print(f"Error: {response.status_code}")
        return []

def create_post(post_data):
    headers = {"Content-Type": "application/json"}
    response = requests.post(url + "posts", data=json.dumps(post_data), headers=headers)
    return response

def get_id(username):
    response = requests.get(url + f"users/{username}")
    if response.status_code == 200:
        user = response.json()
        return user["id"]
    else:
        print(f"Error: {response.status_code}")
        return None

def join_plan(post_id, user_id):
    headers = {"Content-Type": "application/json"}
    participant_data = {"user_id": user_id}
    response = requests.post(url + f"posts/{post_id}/join", data=json.dumps(participant_data), headers=headers)
    return response

def create_user(name):
    headers = {"Content-Type": "application/json"}
    user_data = {"username": name}
    response = requests.post(url + "users", data=json.dumps(user_data), headers=headers)
    return response

def get_user_posts(user_id):
    response = requests.get(url + f"users/{user_id}/posts")
    if response.status_code == 200:
        posts = response.json()
        return posts
    else:
        print(f"Error: {response.status_code}")
        return []