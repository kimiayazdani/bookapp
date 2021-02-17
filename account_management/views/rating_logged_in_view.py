import logging
from typing import Optional

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from account_management.models import Rating

logger = logging.getLogger(__name__)


class LoggedInRatingView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def __init__(self):
        super(LoggedInRatingView, self).__init__()
        self.instance = None  # type: Optional[Rating]

    def get(self, request, *args, **kwargs):
        data = self._get_objects()
        if data:
            return Response(data={'prev_rating': data[0].rate})
        return Response(data={'prev_rating': None})

    def _get_objects(self):
        scored_username = self.kwargs.get('username')
        return Rating.objects.filter(
            scored__username=scored_username, scorer=self.request.user
        )
