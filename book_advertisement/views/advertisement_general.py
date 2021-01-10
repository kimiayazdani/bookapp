import logging
from datetime import datetime, timedelta

from django.core.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from django_plus.api import UrlParam as _p
from rest_framework import permissions
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from book_advertisement.models import BookAd
from book_advertisement.serializers.ad_serializers import (
    BookAdSerializer,
    BookAdUpdateSerializer,
    BookAdListSerializer,
    BookAdSerializerPost,
    AdAll
)

logger = logging.getLogger(__name__)


class ListFreePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'list':  # create new user by anyone
            return True
        return bool(request.user and request.user.is_authenticated)


class BookAdvertiseView(ModelViewSet):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (ListFreePermission,)
    filter_backends = (DjangoFilterBackend,)
    list_params_template = [
        _p('start', _p.datetime, default=datetime.now() - timedelta(days=90)),
        _p('end', _p.datetime, default=datetime.now()),
        _p('ad_type', _p.list(separator=',', item_cleaner=_p.string)),
        _p('min_price', _p.int),
        _p('max_price', _p.int)
    ]

    def get_serializer_class(self):
        if self.request.method == 'GET' and self.action == 'list':
            return BookAdListSerializer
        elif self.request.method == 'PATCH':
            return BookAdUpdateSerializer
        elif self.request.method == 'POST':
            return BookAdSerializerPost
        return BookAdSerializer

    def get_serializer_context(self):
        if self.request.method == 'GET' and self.action == 'list':
            context = {
                'data': self.get_data(),
                'view': self,
            }
        else:
            context = {
                'user_id': self.request.user.id,
            }
        return context

    def get_data(self):
        data = self.get_queryset()
        data = {d['id']: d for d in data}
        return data

    def get_queryset(self):
        _query = None
        if self.request.method == 'GET' and self.action == 'list':
            _query = BookAd.objects.filter(
                status=BookAd.APPROVED
            )
            params = _p.clean_data(self.request.query_params, self.list_params_template)
            start = params['start']
            end = params['end']
            ad_types = params['ad_type']
            min_price = params['min_price']
            max_price = params['max_price']
            validation_kinds = self.validate_kinds(ad_types)
            if start > end:
                raise ValidationError('start datetime should be before end datetime')
            if not validation_kinds:
                raise ValidationError('kind should be in cat, dog or hamster ')
            _query = _query.filter(
                created__gte=start, created__lte=end,
            )
            if ad_types:
                _query = _query.filter(kind__in=ad_types)
            if max_price:
                _query = _query.filter(price__lte=max_price)
            if min_price:
                _query = _query.filter(price__gte=min_price)
            _query = _query.values(
                'id', 'ad_type', 'title', 'price', 'description', 'author__username', 'poster', 'authorName'
            )
        elif self.request.method == 'PATCH':
            _query = BookAd.objects.all()
        _query = self.slice_queryset(_query)
        return _query

    @staticmethod
    def validate_kinds(kinds):
        if kinds is None:
            return True
        for kind in kinds:
            if kind not in BookAd.AD_KINDS:
                return False
        return True

    def slice_queryset(self, queryset):
        offset = self.request.query_params.get('offset', 0)
        limit = self.request.query_params.get('limit', None)
        if limit is not None:
            return queryset[int(offset):int(limit)]
        return queryset

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs['pk']
        try:
            book_ad = BookAd.objects.get(id=pk)
        except BookAd.DoesNotExist:
            return Response(data={'object with id:{} does not exist'.format(pk)}, status=status.HTTP_404_NOT_FOUND)
        serializer = BookAdSerializer(book_ad)
        data = serializer.data
        return Response(data=data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            post = BookAd.objects.get(id=pk)
        except BookAd.DoesNotExist:
            return Response(data={'object with id:{} does not exist'.format(pk)}, status=status.HTTP_404_NOT_FOUND)
        self.perform_destroy(post)
        return Response(data={'object deleted successfully'}, status=status.HTTP_200_OK)


class GetAllUserPosts(ListAPIView):
    authentication_classes = (JWTAuthentication,)
    serializer_class = AdAll

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance = None  # type: Optional[BookAd]

    def get_queryset(self):
        return BookAd.objects.filter(author=self.request.user)


class GetPublicUserPosts(ListAPIView):
    authentication_classes = ()
    serializer_class = AdAll

    def get_queryset(self):
        return BookAd.objects.filter(author__username=self.kwargs.get('username'), status=BookAd.APPROVED)
