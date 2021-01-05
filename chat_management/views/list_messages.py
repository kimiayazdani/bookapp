import logging
from typing import Optional

from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import LimitOffsetPagination
from chat_management.serializers import ListSerializer
from chat_management.models import Message

logger = logging.getLogger(__name__)


class ListMessageView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (JWTAuthentication, )
    serializer_class = ListSerializer
    pagination_class = LimitOffsetPagination

    def __init__(self):
        super(ListMessageView, self).__init__()
        self.instance = None  # type: Optional[Message]

    def get_queryset(self):
        return Message.objects.filter(sender=self.request.user).distinct('receiver')

