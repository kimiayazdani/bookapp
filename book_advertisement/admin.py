from django.contrib import admin

# Register your models here.
from .models import BookAd
from simple_history_field_track.admin import SimpleAdminDiffHistory
from import_export.admin import ExportActionMixin

@admin.register(BookAd)
class BookAdAdmin(SimpleAdminDiffHistory, ExportActionMixin):
    list_display = ('pk', 'author', 'title', 'ad_type', 'authorName', 'status')
    search_fields = ('pk', 'authorName', 'status')
    readonly_fields = ('pk', )
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


