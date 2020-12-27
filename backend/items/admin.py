from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from import_export.admin import ImportExportMixin
from items.models import Category, SubCategory, Item, Tag
from items.resources import ItemResource

class SubCategoryInlineAdmin(admin.TabularInline):
    model = SubCategory

    def has_delete_permission(self, request, obj=None):
        return False


class SubCategoryAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'category', 'subcategory']
    class Meta:
        model = SubCategory

    def has_add_permission(self, request, obj=None):
        return False

class CategoryAdmin(ImportExportMixin, admin.ModelAdmin):
    inlines = [SubCategoryInlineAdmin]
    list_display = ['id','category']
    history_list_display =  ['id','category']
    readonly_fields = ['category']
    list_display_links = ['category']
    list_per_page = 25

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
        
    class Meta:
        model = Category

class TagInlineAdmin(admin.TabularInline):
    model = Tag

class ItemAdmin(ImportExportMixin, SimpleHistoryAdmin):
    inlines = [TagInlineAdmin]
    resource_class = ItemResource
    list_display = ['id', 'item_name', 'available_quantity', 'item_unit', 'rate']
    history_list_display =  ['id', 'item_name', 'category', 'subcategory',
                                'available_quantity', 'item_unit', 'rate']
    list_editable = ['rate']
    search_fields = ['item_name']
    list_per_page = 25
        
    class Meta:
        model = Item

admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)


