import base64
from django.core.exceptions import ValidationError

from django.contrib.auth.hashers import make_password
from django.core.files import File
from rest_framework import serializers
from django.db import transaction

from .models import Account, Rating


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
        fields = ['pk', 'avatar', 'email', 'is_staff', 'bio', 'phone_number', 'username', 'name', 'is_active']

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


class PostRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = (
            'id',
            'scorer',
            'scored',
            'rate',
            'created',
        )
        read_only_fields = ('id', 'created', 'scorer', 'scored')
        writeable_fields = ('rate',)

    def validate(self, attrs):
        print(attrs)
        rate = attrs.get('rate', None)
        if rate is None:
            raise serializers.ValidationError("rate could not be empty")
        return attrs

    def create(self, validated_data):
        create_data = {
            'scorer': self.context['data'].get('scorer'),
            'scored': Account.objects.get(username=self.context['data'].get('scored')),
            'rate': validated_data['rate'],
        }
        ratings = Rating.objects.filter(
                scorer=self.context['data'].get('scorer'),
                scored=Account.objects.get(username=self.context['data'].get('scored'))
        )
        if ratings.count() > 1:
            ratings.delete()
            raise serializers.ValidationError('you could not have more than one vote per each pair we will delete all')

        elif ratings.count() == 1:
            rating = ratings[0]
            rating.rate = validated_data['rate']
            rating.save()
        else:
            with transaction.atomic():
                try:
                    rating = Rating.objects.create(**create_data)
                except ValidationError as e:
                    raise serializers.ValidationError(*e)
        return rating
