from django.urls import path
from django.conf.urls import url

from account_management.views import (
    registration_view,
    Login,
    account_properties_view,
    update_account_view,
    does_account_exist_view,
    ChangePasswordView,
    update_account_picture,
    Logout,
    AccountPublicView
)

app_name = 'account_management'

urlpatterns = [
    path('check_if_account_exists/', does_account_exist_view, name="check_if_account_exists"),
    path('change_password/', ChangePasswordView.as_view(), name="change_password"),
    path('properties/', account_properties_view, name="properties"),
    path('update/', update_account_view, name="update"),
    path('update/avatar/', update_account_picture, name="update_picture"),
    path('login/', Login.as_view(), name="login"),
    path('register/', registration_view, name="register"),
    path('logout/', Logout.as_view(), name='logout'),
    url(r'^show/(?P<username>[0-9a-zA-Z]+)/?$', AccountPublicView.as_view(), name='show_account')
]
