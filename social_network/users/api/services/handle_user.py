from django.utils import timezone


def change_user_last_request_time(user):
    user.last_request = timezone.now()
    user.save()