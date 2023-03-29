from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView

from .serializers import PostSerializer, LikeAnalyticSerializer
from .services import handle_post, handle_like

from users.api.utils import BaseAPIView


class PostApiView(BaseAPIView):
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        if kwargs.get("pk"):
            # details
            post_instance = handle_post.get_instance_by_id(kwargs["pk"])
            serializer = self.serializer_class(instance=post_instance)
        else:
            # all posts
            queryset = handle_post.get_all_posts()
            serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request):
        data = {**request.data, 'user': request.user.id}
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data, status.HTTP_201_CREATED)
        return Response({"error": serializer.errors})

    def patch(self, request, pk):
        post_instance = handle_post.get_instance_by_id(pk)
        serializer = self.serializer_class(instance=post_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": serializer.errors})

    def delete(self, request, pk):

        try:
            handle_post.delete_post_by_id(pk)
            return Response({"message": "successful"}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"error": str(ex)}, status=status.HTTP_403_FORBIDDEN)


@api_view(["POST"])
def like_post(request, post_id):
    try:
        like, created = handle_like.add_post_like(post_id, request.user.id)
        return Response({'like_id': like.id}, status=status.HTTP_201_CREATED)
    except Exception as ex:
        return Response({'message': str(ex)}, status=status.HTTP_403_FORBIDDEN)


@api_view(["POST"])
def unlike_post(request, post_id):
    try:
        handle_like.delete_post_like(post_id, request.user.id)
        return Response({'message': "successful"}, status=status.HTTP_201_CREATED)
    except Exception as ex:
        return Response({'message': str(ex)}, status=status.HTTP_403_FORBIDDEN)


class LikeAnalyticApiView(ListAPIView):
    serializer_class = LikeAnalyticSerializer

    def get_queryset(self):
        start_date = self.request.GET.get("date_from")
        end_date = self.request.GET.get("date_to")
        print(start_date, end_date)
        return handle_like.get_like_analytic_for_dates(start_date, end_date)
