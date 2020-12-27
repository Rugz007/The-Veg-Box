from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from import_export.admin import ImportExportMixin
from sales.models import Address, OrderItem, Order
from django.db.models import Sum, F


class OrderItemInlineAdmin(admin.TabularInline):
    model = OrderItem
    extra = 0
    min_num = 1
    search_fields = ['item']
    autocomplete_fields = ['item']
    def get_fields(self, request, obj=None):
        if obj:
            return ['get_item', 'get_quantity', 'get_item_rate', 'get_discounted_rate', 'extra_info',
                    'get_subtotal']
        else:
            return ['item', 'quantity', 'get_rate', 'discounted_rate', 'extra_info',
                    'get_subtotal']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['get_item', 'get_item_rate', 'get_subtotal', 'get_quantity', 'get_discounted_rate', 'extra_info']
        else:
            return ['get_rate', 'get_subtotal']

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        if obj is None:
            return True
        return False

    def get_rate(self, obj):
        if obj.item_rate is None:
            return obj.item.rate
        return obj.item_rate
    get_rate.short_description = 'Rate'


class OrderAdmin(ImportExportMixin, SimpleHistoryAdmin):
    inlines = [OrderItemInlineAdmin]
    list_display = ['id', 'customer_name', 'customer_phone', 'total', 'mode_of_payment', 'order_status', 'biller']
    history_list_display = ['id', 'biller', 'ordered_by', 'created_at', 'ordered_at', 'customer_name', 'customer_phone' 'shipping_address',
                            'order_status', 'refund_reason']
    search_fields =['customer_name', 'customer_phone']
    fieldsets = [
        ('Order Details', {
            'classes': ('extrapretty'),
            'fields': [('get_order_id', 'biller', 'created_at'), ('customer_name', 'customer_phone'), ('order_status', 'mode_of_payment', 'total'), 'store_cancelled_reason']
        }),
        ('Delivery Details', {
            'classes': ('collapse', 'extrapretty'),
            'fields': [('ordered_by', 'ordered_at', 'shipping_address'), 'refund_reason']
        }),
    ]
    readonly_fields = ['biller', 'ordered_by',
                       'created_at', 'ordered_at', 'get_order_id', 'total']
    list_per_page = 50

    change_form_template = 'admin/sales/sales_change_form.html'

    def has_delete_permission(self, request, obj=None):
        return False

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            try:
                total_1 = OrderItem.objects.filter(
                    order__exact=obj.pk, discounted_rate=None).aggregate(sum=Sum(F('quantity')*F('item_rate')))
                total_2 = OrderItem.objects.filter(
                    order__exact=obj.pk, discounted_rate__lte=0).aggregate(sum=Sum(F('quantity')*F('item_rate')))
                total_3 = OrderItem.objects.filter(
                    order__exact=obj.pk, discounted_rate__gt=0).aggregate(sum=Sum(F('quantity')*F('discounted_rate')))
                if total_1['sum'] is None:
                    total_1['sum'] = 0
                if total_2['sum'] is None:
                    total_2['sum'] = 0
                if total_3['sum'] is None:
                    total_3['sum'] = 0
                obj.total = total_1['sum'] + total_2['sum'] + total_3['sum']
                obj.save()
            except:
                pass
        return form

    def save_formset(self, request, form, formset, change):
        for inline_form in formset.forms:
            if inline_form.has_changed():
                inline_form.instance.item_rate = inline_form.instance.item.rate
        super().save_formset(request, form, formset, change)

    def save_model(self, request, obj, form, change):
        if request.user.user_type == 'ADMIN':
            obj.biller = request.user
        obj.save()


class OrderItemAdmin(ImportExportMixin, SimpleHistoryAdmin):
    list_display = ['order_id', 'ordered_by', 'item', 'quantity']
    history_list_display = ['order', 'item', 'quantity']
    list_per_page = 50

    def has_delete_permission(self, request, obj=None):
        return False

    def order_id(self, obj):
        return obj.order.id

    def ordered_by(self, obj):
        return obj.order.ordered_by
    
    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)


# class AddressAdmin(ImportExportMixin, SimpleHistoryAdmin):
#     list_display = ['id', 'user', 'street_address',
#                     'apartment_address', 'zip', 'default']
#     list_filter = ['default']
#     search_fields = ['user', 'street_address', 'apartment_address']
#     history_list_display = ['id', 'user', 'street_address',
#                             'apartment_address', 'zip', 'default']
#     list_per_page = 50

#     def has_delete_permission(self, request, obj=None):
#         return False

# admin.site.register(Address, AddressAdmin)
