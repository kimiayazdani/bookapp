from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from . import settings
from rest_framework_simplejwt import views as jwt_views
from django.contrib.staticfiles.urls import static
from account_management.views import VerifyEmail

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls'), name='rest_framework'),
    path('api/v1/book-advertise/', include('book_advertisement.urls_v1')),
    path('api/v1/account/', include('account_management.urls_v1')),
    path('api/v1/chat/', include('chat_management.urls')),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('verify-email/', VerifyEmail.as_view(), name='verify-email')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
