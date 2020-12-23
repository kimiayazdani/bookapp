from collections import OrderedDict

from django.db import transaction
from rest_framework import serializers

from account_management.models import Account
from book_advertisement.models import BookAd
from django.core.files import File
import base64
import os
from django.conf import settings


class NestedAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            'id',
            'username',
            'phone_number',
            'email'
        )


class BookAdSerializerPost(serializers.ModelSerializer):
    ad_type = serializers.CharField(default=BookAd.SALE)
    author = NestedAccountSerializer(allow_null=True, required=False)
    poster = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = BookAd
        fields = [
            'id', 'ad_type', 'title', 'description', 'author',
            'poster', 'price', 'authorName'
        ]
        read_only_fields = ('id',)

    def get_user_id(self):
        return self.context['user_id']

    def validate(self, attrs):
        id = self.get_user_id()
        attrs['author'] = Account.objects.get(id=id)
        ad_type = attrs['ad_type']
        poster = attrs.get('poster', None)
        if poster is None:
            attrs.pop('poster')
        if ad_type == BookAd.BUY and poster:
            raise serializers.ValidationError(
                {
                    'ad_type':
                        'پست خرید نمی‌تواند عکس داشته باشد.'
                }
            )
        return attrs

    def create(self, validated_data):
        return BookAd.objects.create(
            **validated_data
        )


class BookAdSerializer(serializers.ModelSerializer):
    ad_type = serializers.CharField(default=BookAd.SALE)
    author = NestedAccountSerializer(allow_null=True, required=False)
    poster = serializers.SerializerMethodField(required=False, allow_null=True)

    class Meta:
        model = BookAd
        fields = [
            'id', 'ad_type', 'title', 'description', 'author',
            'poster', 'price', 'authorName'
        ]
        read_only_fields = ('id',)

    def get_user_id(self):
        return self.context['user_id']

    def get_poster(self, obj):
        if obj.poster == "":
            return ""
        f = open(obj.poster.path, 'rb')
        image = File(f)
        data = base64.b64encode(image.read())
        return data


class BookAdUpdateSerializer(serializers.ModelSerializer):
    """
        this serializer used for PATCH request
    """
    poster = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = BookAd
        fields = (
            'id',
            'title',
            'description',
            'ad_type',
            'poster',
            'price',
            'authorName'
        )
        writable_fields = ('title', 'description', 'tags', 'tags_image', 'kind')

    def get_poster(self, obj):
        if obj.poster is None:
            return None

        f = open(obj.poster.path, 'rb')
        image = File(f)
        data = base64.b64encode(image.read())
        return data

    def update(self, instance: BookAd, validated_data):
        with transaction.atomic():
            for field in self.Meta.writable_fields:
                if field in validated_data:
                    setattr(instance, field, validated_data[field])
            instance.save()
            return super(BookAdUpdateSerializer, self).update(instance, validated_data)


class BookAdListSerializer(serializers.ModelSerializer):
    """
        this serializer used for GET request with action:list
    """
    author__username = serializers.CharField(write_only=True, required=False)
    poster = serializers.SerializerMethodField()

    class Meta:
        model = BookAd
        context_fields = (
            'id',
            'title',
            'author__username',
            'poster',
            'price',
            'ad_type',
            'authorName'
        )
        fields = context_fields
        read_only_fields = context_fields

    def to_representation(self, instance):
        base64_poster = None
        if instance['poster'] != '':
            poster = os.path.join(settings.MEDIA_ROOT, instance['poster'])
            f = open(poster, 'rb')
            image = File(f)
            base64_poster = base64.b64encode(image.read())
        ret = OrderedDict()
        fields = self.Meta.context_fields
        for field in fields:
            if field in self.Meta.fields:
                if field == 'poster' and base64_poster is not None:
                    ret[field] = base64_poster
                else:
                    ret[field] = self.context['data'][instance['id']][field]
        return ret
