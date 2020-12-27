from django.urls import path
from items.views import ItemsListView

urlpatterns = [
    path('', ItemsListView.as_view()),
]