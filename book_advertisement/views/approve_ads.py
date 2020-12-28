import logging
from typing import Optional

from rest_framework_simplejwt.authentication import JWTAuthentication
from book_advertisement.models import BookAd
from rest_framework.generics import UpdateAPIView
from rest_framework import permissions
from book_advertisement.serializers import ApproveAdd

logger = logging.getLogger(__name__)


class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff


class BookAdvertiseApproveView(UpdateAPIView):
    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsStaff, )
    serializer_class = ApproveAdd
    model = BookAd

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance = None  # type: Optional[BookAd]

    def get_queryset(self):
        return BookAd.objects.all()

    def get_object(self):
        if self.instance is None:
            self.instance = super().get_object()
        return self.instance

    def get_serializer_class(self):
        return ApproveAdd
