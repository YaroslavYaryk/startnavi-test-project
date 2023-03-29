from django.urls import path

from .views import PostApiView, like_post, unlike_post, LikeAnalyticApiView

urlpatterns = [
    # post
    path("posts/", PostApiView.as_view(), name="get_all_posts"),
    path("posts/<pk>/", PostApiView.as_view(), name="get_one_post"),
    path("posts/", PostApiView.as_view(), name="create_one_post"),
    path("posts/<pk>/", PostApiView.as_view(), name="edit_one_post"),
    path("posts/<pk>/", PostApiView.as_view(), name="delete_one_post"),

    # like
    path("posts/<post_id>/like/", like_post, name="like post"),
    path("posts/<post_id>/unlike/", unlike_post, name="unlike post"),

    # analytics
    path("analytics/", LikeAnalyticApiView.as_view(), name="get likes analytics"),

]
