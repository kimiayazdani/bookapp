from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from account_management.serializers import PostRatingSerializer


class PostRatingView(CreateAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = PostRatingSerializer

    def get_serializer_context(self):
        ctx = super(PostRatingView, self).get_serializer_context()
        data = {
            'scorer': self.request.user,
            'scored': self.kwargs['username']
        }
        ctx.update(data=data)
        return ctx
