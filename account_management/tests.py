from account_management.views import Login, ChangePasswordView, registration_view
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.test import force_authenticate, APIRequestFactory
from django.test import TestCase
from account_management.models import Account


class TestAccount(TestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        Account.objects.create_user(email='testemail@gmail.com', username='testuser', password='TestUser123')
        user = {
                'username': 'testuser2',
                'email': 'testuser2@gmail.com',
                'password': 'TestUser123'
            }
        self.user = Account.objects.create_user(**user)



    def test_register_account(self):
        request = self.factory.post(
            'api/v1/account/register/',
            data={
                'user': 'mytest@gmail.com',
                'name': 'testtest123',
                'pass': 'Testest123',
                'number': '000'
            },
            format='json'
        )
        view = registration_view
        res = view(request)
        self.token = res.data['token']

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['username'], 'testtest123')

    def test_validate_email(self):
        request = self.factory.post(
            'api/v1/account/register/',
            data={
                'user': 'testemail@gmail.com',
                'name': 'testtfest123',
                'pass': 'Testesft123',
                'number': '09121000000'
            },
            format='json'
        )
        res = registration_view(request)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.data['error_message'], 'That email is already in use.')

    def test_validate_password(self):
        request = self.factory.post(
            'api/v1/account/register/',
            data={
                'user': 'test@gmail.com',
                'name': 'testtfest123',
                'pass': 'test123',
                'number': '9012'
            },
            format='json'
        )
        res = registration_view(request)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res.data['error_message'], 'your password must contain at least one uppercase alphabet.')

    def test_login_account(self):
        request = self.factory.post(
            'api/v1/account/login/',
            data={
                'user': 'testuser2@gmail.com',
                'pass': 'TestUser123'
            },
            format='json'
        )
        view = Login.as_view()
        res = view(request)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['email'], 'testuser2@gmail.com')

    def test_obtain_token(self):
        request = self.factory.post(
            '/api-token-auth/',
            data={
                'username': 'testuser2@gmail.com',
                'password': 'TestUser123'
            },
            format='json'
        )
        view = obtain_auth_token
        res = view(request)
        self.assertEqual(res.status_code, 200)
        self.assertListEqual(list1=list(res.data.keys()), list2=['token'])

    def test_change_password(self):
        request = self.factory.put(
            'api/v1/account/change_password/',
            data={
                'old_password': 'TestUser123',
                'new_password': 'TestUser1234',
                'confirm_new_password': 'TestUser1234'
            },
            format='json'
        )
        force_authenticate(request, self.user)
        view = ChangePasswordView.as_view()
        res = view(request)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['response'],  'successfully changed password')
