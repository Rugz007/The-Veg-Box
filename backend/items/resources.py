from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget
from items.models import Category, SubCategory, Item, Tag
from units.models import Unit

class ItemResource(resources.ModelResource):
    category = fields.Field(
        column_name='category',
        attribute='category',
        widget=ForeignKeyWidget(Category, 'category'))
    subcategory = fields.Field(
        column_name='subcategory',
        attribute='subcategory',
        widget=ForeignKeyWidget(SubCategory, 'subcategory'))
    item_unit = fields.Field(
        column_name='item_unit',
        attribute='item_unit',
        widget=ForeignKeyWidget(Unit, 'unit'))

    class Meta:
        model = Item