import logging
import os
import base64
from collections import defaultdict, OrderedDict
from typing import Optional

from django.conf import settings
from django.core.files import File
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from operator import getitem

from chat_management.models import Message

logger = logging.getLogger(__name__)


class ListMessageView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def __init__(self):
        super(ListMessageView, self).__init__()
        self.instance = None  # type: Optional[Message]

    def get(self, request, *args, **kwargs):
        data = self._get_objects(username=request.user.username)
        return Response(data=data)

    @staticmethod
    def _get_objects(username):
        data = defaultdict()
        first_query = Message.objects.filter(sender__username=username).distinct('receiver').values(
            'receiver__username',
            'receiver__avatar',
            'text',
            'created'
        )
        for data_query in first_query:
            poster = os.path.join(settings.MEDIA_ROOT, data_query['receiver__avatar'])
            print(data_query['receiver__username'])
            f = open(poster, 'rb')
            image = File(f)
            base64_poster = base64.b64encode(image.read())
            data[data_query['receiver__username']] = {
                'text': data_query['text'],
                'sender': username,
                'receiver': data_query['receiver__username'],
                'created': data_query['created'],
                'avatar': base64_poster
            }
        second_query = Message.objects.filter(receiver__username=username).distinct('sender').values(
            'sender__username',
            'sender__avatar',
            'text',
            'created'
        )
        for data_query in second_query:
            if data_query['sender__username'] in data:
                if data[data_query['sender__username']]['created'] > data_query['created']:
                    continue
            poster = os.path.join(settings.MEDIA_ROOT, data_query['sender__avatar'])
            f = open(poster, 'rb')
            image = File(f)
            base64_poster = base64.b64encode(image.read())
            data[data_query['sender__username']] = {
                'text': data_query['text'],
                'sender': data_query['sender__username'],
                'receiver': username,
                'created': data_query['created'],
                'avatar': base64_poster
            }
        res = OrderedDict(sorted(data.items(),
                                 key=lambda x: getitem(x[1], 'created'), reverse=True))
        return res
