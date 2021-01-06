from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from account_management.models import Account


class Login(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        context = {}
        email = request.data.get('username')
        password = request.data.get('password')
        account = authenticate(email=email, password=password)
        if account:
            context['response'] = 'Successfully authenticated.'
            context['pk'] = account.pk
            context['email'] = email.lower()
            context['image'] = str(account.avatar)
            token = RefreshToken.for_user(user=account)
            context['refresh_token'] = str(token)
            context['access_token'] = str(token.access_token)
            return Response(data=context, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN, data={'message': 'نام کاربری یا رمز عبور اشتباه است'})


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([JWTAuthentication, ])
def does_account_exist_view(request):
    if request.method == 'GET':
        email = request.GET['email'].lower()
        data = {}
        try:
            Account.objects.get(email=email)
            data['response'] = 'account with email: {email} exists'.format(email=email)
        except Account.DoesNotExist:
            data['response'] = "Account does not exist"
            return Response(data=data, status=status.HTTP_403_FORBIDDEN)
        return Response(data, status=status.HTTP_501_NOT_IMPLEMENTED)
