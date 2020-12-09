# Generated by Django 2.2.8 on 2020-12-09 22:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='زمان ساخت')),
                ('modified', models.DateTimeField(auto_now=True, db_index=True, verbose_name='آخرین زمان تغییر')),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='email')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('bio', models.CharField(default='new to Happy-animals', max_length=100)),
                ('avatar', models.ImageField(default='default_avatar.png', upload_to='')),
                ('phone_number', models.CharField(max_length=11, verbose_name='شماره تماس ')),
            ],
            options={
                'verbose_name_plural': 'اکانت\u200cها',
                'verbose_name': 'اکانت',
            },
        ),
        migrations.CreateModel(
            name='HistoricalAccount',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('created', models.DateTimeField(blank=True, db_index=True, editable=False, verbose_name='زمان ساخت')),
                ('modified', models.DateTimeField(blank=True, db_index=True, editable=False, verbose_name='آخرین زمان تغییر')),
                ('email', models.EmailField(db_index=True, max_length=60, verbose_name='email')),
                ('username', models.CharField(db_index=True, max_length=30)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('bio', models.CharField(default='new to Happy-animals', max_length=100)),
                ('avatar', models.TextField(default='default_avatar.png', max_length=100)),
                ('phone_number', models.CharField(max_length=11, verbose_name='شماره تماس ')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical اکانت',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
