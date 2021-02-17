import logging
from typing import Optional

from django.db.models import Sum
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from account_management.models import Rating

logger = logging.getLogger(__name__)


class RatingView(GenericAPIView):
    permission_classes = ()
    authentication_classes = ()

    def __init__(self):
        super(RatingView, self).__init__()
        self.instance = None  # type: Optional[Rating]

    def get(self, request, *args, **kwargs):
        data = self._get_objects()
        sum_rating = data.aggregate(Sum('rate'))
        count = data.count()
        if sum_rating['rate__sum'] is not None:
            average_sum = round(sum_rating['rate__sum'] / count, 2)
        else:
            average_sum = 0
        return Response(data={'rating': average_sum, 'number_rating': count})

    def _get_objects(self):
        scored_username = self.kwargs.get('username')
        return Rating.objects.filter(
            scored__username=scored_username
        )
