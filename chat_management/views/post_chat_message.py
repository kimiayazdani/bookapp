from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from chat_management.serializers import PostMessageSerializer


class PostChatMessageView(CreateAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = PostMessageSerializer

    def get_serializer_context(self):
        ctx = super(PostChatMessageView, self).get_serializer_context()
        data = {
            'sender': self.request.user,
            'receiver': self.kwargs['username']
        }
        ctx.update(data=data)
        return ctx
