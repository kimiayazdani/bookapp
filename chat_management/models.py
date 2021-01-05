from django.db import models
from account_management.models import Account
from _helpers.db import TimeModel


class Message(TimeModel):
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='send_messages', verbose_name='فرستنده')
    receiver = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='received_messages', verbose_name='گیرنده')
    text = models.CharField(max_length=500, verbose_name='متن')

    class Meta:
        verbose_name = 'پیام'
        verbose_name_plural = 'پیام‌ها'
