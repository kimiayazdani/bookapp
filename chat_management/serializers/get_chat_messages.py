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

    def to_representation(self, instance):
        data = {
            'sender': instance.sender.username,
            'receiver': instance.receiver.username,
            'text': instance.text,
            'created': instance.created
        }
        return data
