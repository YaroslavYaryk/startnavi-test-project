from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.db.models.functions import TruncDay

from blog.models import PostLike


def get_user_like_for_post(post_id, user_id):
    return get_object_or_404(PostLike, post_id=post_id, user_id=user_id)


def get_all_post_likes(post_id):
    return PostLike.objects.filter(post_id=post_id)


def delete_post_like(post_id, user_id):
    get_user_like_for_post(post_id, user_id).delete()


def add_post_like(post_id, user_id):
    return PostLike.objects.get_or_create(user_id=user_id, post_id=post_id)


def filter_queryset_by_dates(start_date, end_date):
    return PostLike.objects.filter(created_at__range=[start_date, end_date]).order_by("created_at")


def get_like_analytic_for_dates(start_date, end_date):
    filtered_queryset_by_dates = filter_queryset_by_dates(start_date, end_date)
    return filtered_queryset_by_dates.values(
        date=TruncDay("created_at")).annotate(likes=Count("post"))
