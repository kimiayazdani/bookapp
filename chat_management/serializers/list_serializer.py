import base64

from django.core.files import File
from rest_framework import serializers

from account_management.models import Account
from chat_management.models import Message


class NestedAccountSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField(required=False, allow_null=True)

    class Meta:
        model = Account
        fields = (
            'id',
            'username',
            'phone_number',
            'avatar'
        )

    def get_avatar(self, obj):
        if obj.avatar == "":
            return ""
        f = open(obj.avatar.path, 'rb')
        image = File(f)
        data = base64.b64encode(image.read())
        return data


class ListSerializer(serializers.ModelSerializer):
    receiver = NestedAccountSerializer(allow_null=True, required=False)
    text = serializers.SerializerMethodField(source='text')

    class Meta:
        model = Message
        fields = (
            'id',
            'sender',
            'receiver',
            'text',
            'created'
        )

    def get_text(self, obj):
        if len(obj.text) > 10:
            return obj.text[:10] + '...'
        return obj.text
