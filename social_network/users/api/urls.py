from django.urls import path

from rest_framework_simplejwt.views import (
    TokenRefreshView, TokenVerifyView, TokenObtainPairView
)

from .views import CreateUserAPIView, CustomTokenObtainPairView, UserApiView, UserActivityApiView

urlpatterns = [
    # auth
    path("api/user/create/", CreateUserAPIView.as_view(), name="create_user"),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # user
    path("api/user/", UserApiView.as_view(), name="get_user_info"),
    path("api/user/", UserApiView.as_view(), name="change_user_info"),
    path("api/user/activity/", UserActivityApiView.as_view(), name="get_user_activity"),

]
