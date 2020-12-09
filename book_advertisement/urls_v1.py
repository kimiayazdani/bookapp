from django.conf.urls import url, include
from rest_framework import routers

from book_advertisement import views

router = routers.DefaultRouter()
router.register('post', views.BookAdvertiseView, basename='post')

urlpatterns = [

] + router.urls
