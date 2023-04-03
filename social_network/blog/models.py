from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField(max_length=1000)

    user = models.ForeignKey(get_user_model(), related_name="user_posts", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def likes(self):
        return self.post_likes.all()

    def __str__(self):
        return f"{self.id} - {self.title} - {self.created_at}"


class PostLike(models.Model):
    user = models.ForeignKey(get_user_model(), related_name="user_likes", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="post_likes", on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.post.title} - {self.user}"
