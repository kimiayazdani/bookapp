from django.contrib.auth import logout
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication


class Logout(APIView):
    authentication_classes = (JWTAuthentication,)
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
