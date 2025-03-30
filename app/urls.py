from django.urls import path
from .views import (
    OrderListView,
    OrderCreateView,
    OrderDetailView,
    OrderUpdateView,
    OrderDeleteView,
    RevenueReportView,
    AddOrderItemView,
    DeleteOrderItemView,
    MenuItemCreateView,
)

urlpatterns = [
    path('', OrderListView.as_view(), name='order_list'),
    path('new/', OrderCreateView.as_view(), name='order_create'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('<int:pk>/edit/', OrderUpdateView.as_view(), name='order_update'),
    path('<int:pk>/delete/', OrderDeleteView.as_view(), name='order_delete'),
    path('revenue/', RevenueReportView.as_view(), name='revenue_report'),
    path('items/<int:pk>/add/', AddOrderItemView.as_view(), name='order_item_add'),
    path('items/<int:pk>/delete/', DeleteOrderItemView.as_view(), name='order_item_delete'),
    path('menu-item/new/', MenuItemCreateView.as_view(), name='menu_item_create'),

]
