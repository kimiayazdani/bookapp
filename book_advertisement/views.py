import logging
from datetime import datetime, timedelta

from django.conf import settings
from django.core.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from django_plus.api import UrlParam as _p
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from book_advertisement.models import BookAd
from book_advertisement.serializers.ad_serializers import (
    BookAdSerializer,
    BookAdUpdateSerializer,
    BookAdListSerializer
)

logger = logging.getLogger(__name__)


class BookAdvertiseView(ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    list_params_template = [
        _p('start', _p.datetime, default=datetime.now() - timedelta(days=90)),
        _p('end', _p.datetime, default=datetime.now()),
        _p('ad_type', _p.list(separator=',', item_cleaner=_p.string)),
        _p('price', _p.list(separator=',', item_cleaner=_p.int))
    ]

    def get_serializer_class(self):
        if self.request.method == 'GET' and self.action == 'list':
            return BookAdListSerializer
        elif self.request.method == 'PATCH':
            return BookAdUpdateSerializer
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
            params = _p.clean_data(self.request.query_params, self.list_params_template)
            start = params['start']
            end = params['end']
            ad_types = params['ad_type']
            price = params['price']
            validation_kinds = self.validate_kinds(ad_types)
            if start > end:
                raise ValidationError('start datetime should be before end datetime')
            if not validation_kinds:
                raise ValidationError('kind should be in cat, dog or hamster ')
            _query = BookAd.objects.filter(
                created__gte=start, created__lte=end,
            )
            if ad_types:
                _query = _query.filter(kind__in=ad_types)
            if price:
                _query = _query.filter(price__lte=price)
            _query = _query.values(
                'id', 'ad_type', 'title', 'price', 'description', 'author__username', 'poster'
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
        if book_ad.pet_image:
            image_src = str(book_ad.poster) + settings.MEDIA_URL
        else:
            image_src = None
        data = {
            'id': pk,
            'title': book_ad.title,
            'start': book_ad.description,
            'created': book_ad.created,
            'price': book_ad.price,
            'author': book_ad.author.id,
            'pet_image': image_src,
            'ad_type': book_ad.ad_type
        }
        return Response(data=data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            post = BookAd.objects.get(id=pk)
        except BookAd.DoesNotExist:
            return Response(data={'object with id:{} does not exist'.format(pk)}, status=status.HTTP_404_NOT_FOUND)
        self.perform_destroy(post)
        return Response(data={'object deleted successfully'}, status=status.HTTP_200_OK)
