import json

import requests
from faker import Faker

fake = Faker()


def get_random_user_credentials():
    return {
        "email": fake.email(),
        "password": fake.password()
    }


def get_random_post_credentials():
    result = {
        "title": fake.word(),
        "body": fake.text(500)
    }
    return json.dumps(result)


def create_user(credentials, SERVER_URL):
    r = requests.post(f"{SERVER_URL}auth/api/user/create/", data=credentials)
    if r.status_code == 201:
        return r.json()


def get_tokens_for_user(credentials, SERVER_URL):
    r = requests.post(f"{SERVER_URL}auth/api/token/", data=credentials)
    if r.ok:
        return r.json()


def create_headers_for_request(token):
    return {"Authorization": f"Bearer {token}", 'Content-type': 'application/json'}


def create_post_for_user(post_data, token, SERVER_URL):
    headers = create_headers_for_request(token)
    r = requests.post(f"{SERVER_URL}blog/api/posts/create/", data=post_data, headers=headers)
    if r.ok:
        return r.json()


def write_result_to_json(file_type, result, RESULT_FOLDER_PATH):
    with open(f"{RESULT_FOLDER_PATH}/{file_type}.json", "w") as outfile:
        json.dump(result, outfile)


def create_like_to_post(post_id, token, SERVER_URL):
    headers = create_headers_for_request(token)
    r = requests.post(f"{SERVER_URL}blog/api/posts/{post_id}/like/", headers=headers)
    if r.ok:
        return r.json()
