from django.conf.urls import url, include
from rest_framework import routers

from book_advertisement.views import BookAdvertiseView
from book_advertisement.views import BookAdvertiseApproveView

router = routers.DefaultRouter()
router.register('post', BookAdvertiseView, basename='post')

urlpatterns = [
    url(r'^approve/(?P<pk>\d+)/$', BookAdvertiseApproveView.as_view(), name='approve')
] + router.urls
