from django.urls import path

from .views import PostApiView, like_post, unlike_post, LikeAnalyticApiView, PostListAPIView

urlpatterns = [
    # post
    path("posts/", PostListAPIView.as_view(), name="get_all_posts"),
    path("posts/<int:pk>/", PostApiView.as_view(), name="get_one_post"),
    path("posts/create/", PostApiView.as_view(), name="create_one_post"),
    path("posts/<int:pk>/", PostApiView.as_view(), name="edit_one_post"),
    path("posts/<int:pk>/", PostApiView.as_view(), name="delete_one_post"),

    # like
    path("posts/<int:post_id>/like/", like_post, name="like_post"),
    path("posts/<int:post_id>/unlike/", unlike_post, name="unlike_post"),

    # analytics
    path("analytics/", LikeAnalyticApiView.as_view(), name="get_likes_analytics"),

]
