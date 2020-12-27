from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Vendor, PurchaseOrder, PurchaseOrderItem
from django.db.models import Sum, F


class PurchaseOrderItemInline(admin.TabularInline):
    model = PurchaseOrderItem
    extra = 1
    # min_num = 1
    search_fields = ['item']
    autocomplete_fields = ['item']
    def get_fields(self, request, obj=None):
        if obj:
            return ['get_item', 'get_quantity', 'get_expected_error', 'get_cost_price', 'get_subtotal']
        else:
            return ['item', 'quantity', 'expected_error', 'cost_price', 'get_subtotal']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['get_item', 'get_cost_price', 'get_expected_error', 'get_subtotal', 'get_quantity']
        else:
            return ['get_rate', 'get_subtotal']

    def has_add_permission(self, request, obj=None):
        if obj:
            return False
        else:
            return True

class PurchaseOrderAdmin(admin.ModelAdmin):
    inlines = [PurchaseOrderItemInline]
    readonly_fields = ['total']
    list_display = ['id', 'date', 'vendor', 'total', 'paid']
    fieldsets = [
        ('Purchase Order Details', {
            'classes': ('extrapretty'),
            'fields': [('vendor', 'date'), ('total'), ('mode_of_payment', 'paid')]
        })
    ]
    change_form_template = 'admin/purchaseorders/purchaseorders_change_form.html'

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            try:
                total = PurchaseOrderItem.objects.filter(
                    purchase_order__exact=obj.pk).aggregate(sum=Sum(F('quantity')*F('cost_price')))
                if total['sum'] is None:
                    total['sum'] = 0
                obj.total = total['sum']
                obj.save()
            except:
                pass
        return form

    def has_delete_permission(self, request, obj=None):
        return False

class PurchaseOrderItemAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_add_permission(self, request, obj=None):
        return False

class VendorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'info']

admin.site.register(Vendor, VendorAdmin)
admin.site.register(PurchaseOrder, PurchaseOrderAdmin)
admin.site.register(PurchaseOrderItem, PurchaseOrderItemAdmin)
