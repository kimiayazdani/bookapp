from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from account_management.models import Account
from account_management.serializers import AccountPropertiesSerializer


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
def account_properties_view(request):
    try:
        account = request.user
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AccountPropertiesSerializer(account)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

