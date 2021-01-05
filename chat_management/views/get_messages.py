import logging
from typing import Optional

from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from chat_management.models import Message
from chat_management.serializers import MessageSerializer

logger = logging.getLogger(__name__)


class MessageView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    pagination_class = LimitOffsetPagination
    serializer_class = MessageSerializer

    def __init__(self):
        super(MessageView, self).__init__()
        self.instance = None  # type: Optional[Message]

    def get_queryset(self):
        receiver_username = self.kwargs.get('username')
        return Message.objects.filter(sender=self.request.user, receiver__username=receiver_username)
