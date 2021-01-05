from rest_framework import serializers

from chat_management.models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = (
            'id',
            'sender',
            'receiver',
            'text',
            'created'
        )
