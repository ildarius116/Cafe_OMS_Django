from rest_framework import viewsets, permissions
from rest_framework.permissions import BasePermission
from rest_framework.serializers import ModelSerializer
from django.db.models.query import QuerySet
from typing import List
from app.models import Order, MenuItem
from app.serializers import MenuItemSerializer, OrderCreateSerializer, OrderListSerializer


class MenuItemViewSet(viewsets.ModelViewSet):
    """
    Функция управления (CRUD-операции) блюдами меню по API.
    Требует авторизации для любых действий, кроме GET-запросов.
    Позволяет:
    - Просматривать меню (GET)
    - Добавлять новые блюда (POST)
    - Редактировать существующие (PUT/PATCH)
    - Удалять блюда (DELETE)
    """
    queryset: QuerySet[MenuItem] = MenuItem.objects.all()
    serializer_class: ModelSerializer = MenuItemSerializer
    permission_classes: List[BasePermission] = [permissions.AllowAny]


class OrderViewSet(viewsets.ModelViewSet):
    """
    Функция управления заказами по API.
    Требует авторизации для любых действий.
    """
    queryset = Order.objects.all().order_by('-created_at')
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderListSerializer
