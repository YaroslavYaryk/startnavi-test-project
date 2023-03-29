from django.urls import path, include

from users.api import urls as user_api

urlpatterns = [
    path("", include(user_api)),
]
