from django.urls import path
from account_management.views import (
    registration_view,
    Login,
    account_properties_view,
    update_account_view,
    does_account_exist_view,
    ChangePasswordView,
    Logout,
)

app_name = 'account_management'

urlpatterns = [
    path('check_if_account_exists/', does_account_exist_view, name="check_if_account_exists"),
    path('change_password/', ChangePasswordView.as_view(), name="change_password"),
    path('properties', account_properties_view, name="properties"),
    path('update/', update_account_view, name="update"),
    path('login/', Login.as_view(), name="login"),
    path('register/', registration_view, name="register"),
    path('logout/', Logout.as_view(), name='logout'),
]
