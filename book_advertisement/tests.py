from django.test import TestCase
from rest_framework.test import force_authenticate, APIRequestFactory

from account_management.models import Account
from book_advertisement.models import BookAd
from book_advertisement.views import BookAdvertiseView


class TestPostViewSet(TestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        user = {
            'username': 'testuser',
            'email': 'testuser@gmail.com',
            'password': 'TestUser123'
        }
        self.user = Account.objects.create_user(**user)
        self.post = BookAd.objects.create(
            title='test',
            description='test description',
            ad_type='sell',
            author=self.user,
            price = 30000
        )

    def test_create_post(self):
        request = self.factory.post(
            'api/v1/book-advertise/post/',
            data={
                'title': 'create post test',
                'description': 'testtest123',
                'ad_type': 'buy',
                'price': 45000
            },
            format='json'
        )
        view = BookAdvertiseView.as_view({'post': 'create'})
        force_authenticate(request, self.user)
        res = view(request)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data['ad_type'], 'buy')
        self.assertEqual(res.data['price'], 45000)

    def test_get_post(self):
        request = self.factory.get(
            'api/v1/adoption/post/',
        )
        view = BookAdvertiseView.as_view({'get': 'retrieve'})
        force_authenticate(request, self.user)
        res = view(request, pk=self.post.pk)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['ad_type'], 'sell')
        self.assertEqual(res.data['price'], 30000)

    def test_update_post(self):
        request = self.factory.patch(
            'api/v1/adoption/post/',
            data={
                'title': 'new title',
                'ad_type': 'buy'
            },
            format='json'
        )
        view = BookAdvertiseView.as_view({'patch': 'partial_update'})
        force_authenticate(request, self.user)
        res = view(request, pk=self.post.pk)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['ad_type'], 'buy')
        self.assertEqual(res.data['title'], 'new title')
