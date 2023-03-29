from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from .services import handle_user


class BaseAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        try:
            handle_user.change_user_last_request_time(request.user)
        except NotImplementedError:
            # when user is not authenticated it  would go to method
            # and since its IsAuthenticated permission it would
            # raise 401 error
            pass
        return response
