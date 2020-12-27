from rest_framework import serializers
from items.models import Item

class ItemsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ['id', 'item_name', 'rate', 'unit']
    
    unit = serializers.SerializerMethodField('get_item_unit')

    def get_item_unit(self, obj):
        return obj.item_unit.abbreviation