from django.urls import path
from sales.views import AddOrderView, AddOrderItemsView, DeleteOrderItemsView, UpdateOrderView

urlpatterns = [
    path('addorder/', AddOrderView.as_view()),
    path('updateorder/<int:pk>/', UpdateOrderView.as_view()),
    path('addorderitems/', AddOrderItemsView.as_view()),
    path('deleteorderitems/<int:id>/', DeleteOrderItemsView.as_view()),
]