from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework import serializers

from account_management.models import Account
from chat_management.models import Message


class PostMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = (
            'id',
            'sender',
            'receiver',
            'text',
            'created',
        )
        read_only_fields = ('id', 'created', 'sender', 'receiver')
        writeable_fields = ('text',)

    def validate(self, attrs):
        text = attrs.get('text', None)
        if text is None:
            raise serializers.ValidationError("text message could not be empty")
        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            try:
                create_data = {
                    'sender': self.context['data'].get('sender'),
                    'receiver': Account.objects.get(username=self.context['data'].get('receiver')),
                    'text': validated_data['text'],
                }
                message = Message.objects.create(**create_data)
            except ValidationError as e:
                raise serializers.ValidationError(*e)
        return message
