from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from import_export.admin import ImportExportMixin
from accounts.models import UserAccount
from sales.models import Address

class AddressInlineAdmin(admin.TabularInline):
    model = Address

class UserAccountAdmin(ImportExportMixin, SimpleHistoryAdmin):
    inlines = [AddressInlineAdmin]
    list_display = ['id', 'name', 'email', 'phone', 'is_verified']
    list_filter = ['is_verified']
    search_fields = ['name', 'email', 'phone']
    history_list_display = ['is_verified', 'name', 'phone', 'email']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 50

    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_add_permission(self, request, obj=None):
        return False

admin.site.register(UserAccount, UserAccountAdmin)
