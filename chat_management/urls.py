from django.conf.urls import url

from chat_management.views import ListMessageView, MessageView, PostChatMessageView

urlpatterns = [
    url(r'^main-page$', ListMessageView.as_view(), name='main-chat'),
    url(r'^(?P<username>[0-9a-zA-Z]+)/get/?$', MessageView.as_view(), name='get_message'),
    url(r'^(?P<username>[0-9a-zA-Z]+)/post/?$', PostChatMessageView.as_view(), name='post_message'),
]
