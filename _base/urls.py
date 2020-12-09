from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from . import settings
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls'), name='rest_framework'),
    path('api/v1/book-advertise/', include('book_advertisement.urls_v1')),
    path('api/v1/account/', include('account_management.urls_v1')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
