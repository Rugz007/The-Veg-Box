from rest_framework.generics import ListAPIView
from rest_framework import permissions
from items.models import Item
from items.serializers import ItemsListSerializer

class ItemsListView(ListAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = ItemsListSerializer
    queryset = Item.objects.all()