from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ExportActionMixin
from simple_history_field_track.admin import SimpleAdminDiffHistory

from .models import Account, Rating


@admin.register(Rating)
class BookAdAdmin(SimpleAdminDiffHistory, ExportActionMixin):
    list_display = ('pk', 'scorer', 'scored', 'rate')
    search_fields = ('pk', 'scorer', 'scored')
    readonly_fields = ('pk',)
    filter_horizontal = ()
    list_filter = ('scorer',)
    fieldsets = ()


@admin.register(Account)
class AccountAdmin(UserAdmin):
    list_display = ('pk', 'email', 'username', 'created', 'modified', 'is_admin', 'is_active')
    search_fields = ('pk', 'email', 'username')
    readonly_fields = ('pk', 'created', 'last_login',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
