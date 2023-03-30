from services import handle_bot


def sign_up_users():
    try:
        return handle_bot.handle_user_sign_up()
    except Exception as ex:
        print(ex)
        raise ex


def create_posts_by_users(users_json):
    try:
        return handle_bot.handle_create_post_by_user(users_json)
    except Exception as ex:
        print(ex)
        raise ex


def create_likes_for_posts(posts, users):
    try:
        return handle_bot.handle_create_like_for_post(posts, users)
    except Exception as ex:
        print(ex)
        raise ex


if __name__ == "__main__":
    users = sign_up_users()
    posts, user_posts = create_posts_by_users(users)
    likes = create_likes_for_posts(posts, users)
