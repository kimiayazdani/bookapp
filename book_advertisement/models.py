from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from account_management.models import Account

class BookAd(models.Model):
    SALE = 'sale'
    BUY = 'buy'

    AD_CHOICES = (
        (SALE, 'فروش'),
        (BUY, 'خرید'),
    )
    AD_KINDS = tuple(dict(AD_CHOICES).keys())

    poster = models.ImageField(verbose_name="تصویر", upload_to='ad_posters/', null=True, blank=True, )
    title = models.CharField(verbose_name="نام کتاب", max_length=30)
    author = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='نویسنده')
    description = models.TextField(verbose_name="توضیحات", max_length=500)
    ad_type = models.CharField(verbose_name="نوع درخواست", default=SALE, db_index=True, max_length=20)
    price = models.IntegerField(verbose_name="قیمت", default=20000)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('ad', kwargs={'pk': self.pk})

    def clean(self):
        if self.poster and not self.sell:
            raise ValidationError("posters are not allowed for buy advertisements")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(BookAd, self).save(*args, **kwargs)