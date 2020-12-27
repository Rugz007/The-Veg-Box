from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from import_export.admin import ImportExportMixin
from waste.models import Discard, DiscardItem
from django.db.models import Sum, F

class DiscardItemInlineAdmin(admin.TabularInline):
    model = DiscardItem
    extra = 0
    min_num = 1
    search_fields = ['item']
    autocomplete_fields = ['item']
    def get_fields(self, request, obj=None):
        if obj:
            return ['get_item', 'get_quantity', 'get_item_purchase_rate',
                    'reason', 'extra_info', 'get_subtotal']
        else:
            return ['item', 'quantity', 'item_purchase_rate',
                    'reason', 'extra_info', 'get_subtotal']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['get_item', 'get_quantity', 'get_item_purchase_rate',
                    'get_subtotal', 'reason', 'extra_info']
        else:
            return ['get_subtotal']

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        if obj is None:
            return True
        return False



class DiscardAdmin(ImportExportMixin, SimpleHistoryAdmin):
    inlines = [DiscardItemInlineAdmin]
    list_display = ['id', 'discarder', 'total', 'created_at']
    history_list_display = ['id', 'discarder', 'total', 'created_at']
    fieldsets = [
        ('Discard Details', {
            'classes': ('extrapretty'),
            'fields': [('get_discard_id', 'discarder', 'created_at'), 'total']
        }),
    ]
    readonly_fields = ['discarder', 'created_at', 'total', 'get_discard_id']
    list_per_page = 50
    change_form_template = 'admin/waste/waste_change_form.html'


    def has_delete_permission(self, request, obj=None):
        return False

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            try:
                total = DiscardItem.objects.filter(
                    discard__exact=obj.pk).aggregate(sum=Sum(F('quantity')*F('item_purchase_rate')))
                if total['sum'] is None:
                    total['sum'] = 0
                obj.total = total['sum']
                obj.save()
            except:
                pass
        return form

    def save_model(self, request, obj, form, change):
        obj.discarder = request.user
        obj.save()


class DiscardItemAdmin(ImportExportMixin, SimpleHistoryAdmin):
    list_display = ['discard', 'item', 'item_purchase_rate', 'quantity', 'reason', 'extra_info']
    history_list_display = ['discard', 'item', 'item_purchase_rate', 'quantity', 'reason', 'extra_info']
    list_per_page = 50

    def has_delete_permission(self, request, obj=None):
        return False

    def order_id(self, obj):
        return obj.order.id

    def ordered_by(self, obj):
        return obj.order.ordered_by

    def has_add_permission(self, request, obj=None):
        return False

admin.site.register(Discard, DiscardAdmin)
admin.site.register(DiscardItem, DiscardItemAdmin)
