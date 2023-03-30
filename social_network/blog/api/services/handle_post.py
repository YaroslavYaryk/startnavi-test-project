from django.shortcuts import get_object_or_404

from blog.models import Post


def get_instance_by_id(pk):
    return get_object_or_404(Post, pk=pk)


def get_all_posts():
    return Post.objects.all().order_by("created_at")


def delete_post_by_id(pk):
    get_instance_by_id(pk).delete()
