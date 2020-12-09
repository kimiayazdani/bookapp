from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from .serializers import RegistrationSerializer, ChangePasswordSerializer, AccountPropertiesSerializer
from account_management.models import Account
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import logout


class Logout(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            request.user.auth_token.delete()
            logout(request)
            data = {'Response': 'successful'}
            p_status = status.HTTP_200_OK
        except Exception as e:
            data = {'Response': 'could not find user'}
            p_status = status.HTTP_400_BAD_REQUEST
        finally:
            return Response(data=data, status=p_status)


@api_view(['POST', ])
@authentication_classes([])
def registration_view(request):
    data = {}
    email = request.data.get('user', '0').lower()

    if validate_email(email) is not None:
        data['error_message'] = 'That email is already in use.'
        data['response'] = 'Error'
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

    username = request.data.get('name', '0')
    if validate_username(username) is not None:
        data['error_message'] = 'That username is already in use.'
        data['response'] = 'Error'
        return Response(data=data, status=status.HTTP_403_FORBIDDEN)

    password = request.data.get('pass', '0')
    val = validate_password(password)
    if val[0] is None:
        data['error_message'] = val[1]
        data['response'] = 'Error'
        return Response(data, status=status.HTTP_403_FORBIDDEN)
    data = {
        'password': password,
        'email': email,
        'phone_number': request.data.get('number', '0'),
        'username': username
    }
    serializer = RegistrationSerializer(data=data)

    if serializer.is_valid():
        account = serializer.save()
        account.save()
        ser = RegistrationSerializer(account)
        data = ser.data
        token = Token.objects.create(user=account)
        data['userId'] = account.pk
        data['profilePicture'] = account.avatar.url
        data['email'] = account.email
        data['username'] = account.username
        data['token'] = str(token)

        return Response(data=data, status=status.HTTP_200_OK)
    else:
        data = serializer.errors

        return Response(data=data, status=status.HTTP_403_FORBIDDEN)


def validate_email(email):
    try:
        account = Account.objects.get(email=email)
    except Account.DoesNotExist:
        return None
    if account != None:
        return email


def validate_username(username):
    try:
        account = Account.objects.get(username=username)
    except Account.DoesNotExist:
        return None
    if account != None:
        return username


def validate_password(passwd):
    SpecialSym = ['$', '@', '#', '%']
    val = {0: "not None", 1: "not any error"}

    if len(passwd) < 6:
        val[0] = None
        val[1] = 'password is too short!'
        return val
    if len(passwd) > 40:
        val[0] = None
        val[1] = 'Password is too long!!'
        return val
    if not any(char.isdigit() for char in passwd):
        val[0] = None
        val[1] = 'your password must contain at least one digit.'
        return val
    if not any(char.isupper() for char in passwd):
        val[0] = None
        val[1] = 'your password must contain at least one uppercase alphabet.'
        return val
    if not any(char.islower() for char in passwd):
        val[0] = None
        val[1] = 'your password must contain at least one lowercase alphabet.'
        return val

    if any(char in SpecialSym for char in passwd):
        val[0] = None
        val[1] = 'your passwrod shouldn\'t contain any of {@,#,%,$ } set'
        return val
    return val


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def account_properties_view(request):
    try:
        account = request.user
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AccountPropertiesSerializer(account)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT', ])
@permission_classes((IsAuthenticated,))
@authentication_classes((TokenAuthentication,))
def update_account_view(request):
    try:
        account = request.user
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = AccountPropertiesSerializer(account, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = 'Account update success'
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        context = {}
        email = request.data.get('user')
        password = request.data.get('pass')
        account = authenticate(email=email, password=password)
        if account:
            context['response'] = 'Successfully authenticated.'
            context['pk'] = account.pk
            context['email'] = email.lower()
            context['image'] = str(account.avatar)
            context['token'] = str(Token.objects.get_or_create(user=account)[0])
            context['logged_in'] = 1
            return Response(data=context, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN, data={'error': 'user did not find', 'logged_in': 0})


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([TokenAuthentication, ])
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


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = Account
    permission_classes = (IsAuthenticated,)

    authentication_classes = (TokenAuthentication,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            # confirm the new passwords match
            new_password = serializer.data.get("new_password")
            confirm_new_password = serializer.data.get("confirm_new_password")
            if new_password != confirm_new_password:
                return Response({"new_password": ["New passwords must match"]}, status=status.HTTP_400_BAD_REQUEST)

            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({"response": "successfully changed password"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
