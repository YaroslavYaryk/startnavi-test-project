import random

from automated_bot import static_functions
from automated_bot.config import NUMBER_OF_USERS, MAX_LIKES_PER_USER, MAX_POSTS_PER_USER, RESULT_FOLDER_PATH, SERVER_URL


def handle_user_sign_up():
    result_json = []
    for _ in range(NUMBER_OF_USERS):
        credentials = static_functions.get_random_user_credentials()
        try:
            result_1 = static_functions.create_user(credentials, SERVER_URL)
            result_2 = static_functions.get_tokens_for_user(credentials, SERVER_URL)
            result = {**result_1, **result_2}
            result_json.append(result)


        except Exception as ex:
            print(ex)
            raise ex

    try:
        static_functions.write_result_to_json("sign_up", result_json, RESULT_FOLDER_PATH)
    except Exception as ex:
        print(ex)
        raise ex

    return result_json


def handle_create_post_by_user(users_json, ):
    result_json = []
    posts_json = []
    for user in users_json:
        random_post_data = static_functions.get_random_post_credentials()
        random_post_number = random.randint(1, MAX_POSTS_PER_USER)
        user_posts = {user.get("user_id"): []}
        for _ in range(random_post_number):
            try:
                result = static_functions.create_post_for_user(random_post_data, user["access"], SERVER_URL)
                user_posts[user.get("user_id")].append(result)
                posts_json.append(result)
            except Exception as ex:
                print(ex)
                raise ex
        result_json.append(user_posts)

    try:
        static_functions.write_result_to_json("user_posts", result_json, RESULT_FOLDER_PATH)
        static_functions.write_result_to_json("posts", posts_json, RESULT_FOLDER_PATH)
    except Exception as ex:
        print(ex)
        raise ex

    return posts_json, result_json


def handle_create_like_for_post(posts, users):
    like_json = []
    for user in users:
        random_likes_number = random.randint(1, MAX_LIKES_PER_USER)
        new_posts = random.choices(posts, k=random_likes_number)
        for post in new_posts:
            try:

                result = static_functions.create_like_to_post(post["id"], user["access"], SERVER_URL)
                like_json.append(result)
            except Exception as ex:
                print(ex)
                raise ex

    try:
        static_functions.write_result_to_json("likes", like_json, RESULT_FOLDER_PATH)
    except Exception as ex:
        print(ex)
        raise ex

    return like_json
