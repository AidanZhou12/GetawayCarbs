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