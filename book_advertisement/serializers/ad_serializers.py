from collections import OrderedDict

from django.db import transaction
from rest_framework import serializers

from account_management.models import Account
from book_advertisement.models import BookAd


class NestedAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            'id',
            'username',
        )


class BookAdSerializer(serializers.ModelSerializer):
    """
    this serializer used for POST request
    """
    ad_type = serializers.CharField(default=BookAd.SALE)
    author = NestedAccountSerializer(allow_null=True, required=False)

    class Meta:
        model = BookAd
        fields = [
            'id', 'ad_type', 'title', 'description', 'author',
            'poster', 'price'
        ]
        read_only_fields = ('id',)

    def get_user_id(self):
        return self.context['user_id']

    def validate(self, attrs):
        id = self.get_user_id()
        attrs['author'] = Account.objects.get(id=id)
        ad_type = attrs['ad_type']
        poster = attrs['poster']
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


class BookAdUpdateSerializer(serializers.ModelSerializer):
    """
        this serializer used for PATCH request
    """

    class Meta:
        model = BookAd
        fields = (
            'id',
            'title',
            'description',
            'ad_type',
            'poster',
            'price'
        )
        writable_fields = ('title', 'description', 'tags', 'tags_image', 'kind')

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

    class Meta:
        model = BookAd
        context_fields = (
            'id',
            'title',
            'author__username',
            'poster',
            'price'
        )
        fields = context_fields
        read_only_fields = context_fields

    def to_representation(self, instance):

        ret = OrderedDict()
        fields = self.Meta.context_fields
        for field in fields:
            if field in self.Meta.fields:
                ret[field] = self.context['data'][instance['id']][field]
        return ret
