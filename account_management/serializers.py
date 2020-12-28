from rest_framework import serializers
from .models import Account
from django.contrib.auth.hashers import make_password
from django.core.files import File
import base64


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('username', 'email', 'password', 'phone_number')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(RegistrationSerializer, self).create(validated_data)


class AccountPicture(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['pk', 'avatar']
        read_only_fields = ['pk']

    def update(self, instance, validated_data):
        return super(AccountPicture, self).update(instance, validated_data)


class AccountPropertiesSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ['pk', 'avatar', 'email', 'is_staff', 'bio', 'phone_number', 'username', 'name', 'is_validate']

    def get_avatar(self, obj):
        f = open(obj.avatar.path, 'rb')
        image = File(f)
        data = base64.b64encode(image.read())
        return data


class AccountUpdateSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=False)

    class Meta:
        model = Account
        fields = ['pk', 'phone_number', 'bio', 'name', 'username', 'password', 'avatar']
        read_only_fields = ['pk']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def update(self, instance, validated_data):
        if validated_data.get('password', None):
            validated_data['password'] = make_password(validated_data['password'])
        return super(AccountUpdateSerializer, self).update(instance, validated_data)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)
