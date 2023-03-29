from rest_framework import serializers

from blog.models import Post, PostLike


class PostSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = "__all__"

    def get_likes(self, object: Post):
        return object.likes.count()


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = "__all__"


class LikeAnalyticSerializer(serializers.Serializer):
    date = serializers.DateField()
    likes = serializers.IntegerField()
