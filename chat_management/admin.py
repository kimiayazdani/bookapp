from django.contrib import admin
from .models import Message
from simple_history_field_track.admin import SimpleAdminDiffHistory
from import_export.admin import ExportActionMixin


@admin.register(Message)
class BookAdAdmin(SimpleAdminDiffHistory, ExportActionMixin):
    list_display = ('pk', 'sender', 'receiver', 'text')
    search_fields = ('pk', 'sender', 'receiver')
    readonly_fields = ('pk', )
    filter_horizontal = ()
    list_filter = ('sender', )
    fieldsets = ()
