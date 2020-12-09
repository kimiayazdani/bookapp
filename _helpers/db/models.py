from datetime import datetime

from django.db import models
from django.db.models import Manager


class TimeModelManager(Manager):
    def update(self, **kwargs):
        if 'modified' not in kwargs:
            kwargs['modified'] = datetime.now()
        return super().update(**kwargs)

    def bulk_create(self, objs, batch_size=None):
        for obj in objs:
            obj.modified = datetime.now()
        return super().bulk_create(objs, batch_size)


class TimeModel(models.Model):

    objects = TimeModelManager()

    created = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name="زمان ساخت"
    )

    modified = models.DateTimeField(
        auto_now=True,
        db_index=True,
        verbose_name="آخرین زمان تغییر"
    )

    class Meta:
        ordering = ('-created',)
        abstract = True
