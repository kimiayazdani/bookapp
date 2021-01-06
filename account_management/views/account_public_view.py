from rest_framework.generics import RetrieveAPIView

from account_management.models import Account
from account_management.serializers import AccountPropertiesSerializer


class AccountPublicView(RetrieveAPIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = AccountPropertiesSerializer
    lookup_field = 'username'

    def get_queryset(self):
        return Account.objects.filter(username=self.kwargs['username'])
