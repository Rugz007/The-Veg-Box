from django.contrib import admin
from import_export.admin import ImportExportMixin
from simple_history.admin import SimpleHistoryAdmin
from units.models import Unit

class UnitAdmin(ImportExportMixin,SimpleHistoryAdmin):
    list_display = ['id', 'unit', 'abbreviation']
    history_list_display = ['id', 'unit', 'abbreviation']
    list_display_links = ['unit']
    list_per_page = 25

    class Meta:
        model = Unit

admin.site.register(Unit, UnitAdmin)
