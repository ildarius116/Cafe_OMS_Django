from django import forms
from django.db.models import Model
from django.db.models.query import QuerySet
from rest_framework import viewsets, permissions
from rest_framework.permissions import BasePermission
from rest_framework.serializers import ModelSerializer
from typing import Any, Dict, List
from .models import Order, OrderItem, MenuItem
from .serializers import MenuItemSerializer, OrderListSerializer


class OrderForm(forms.ModelForm):
    """
    Класс создания/редактирования заказов.

    Поля:
        table_number - 'Номер стола' - числовое поле с CSS-классом form-control;
        status - 'Статус заказа' - выпадающий список с CSS-классом form-control.
    """

    class Meta:
        model: Model = Order
        fields: List[str] = ['table_number', 'status']
        labels: Dict[str, str] = {
            'table_number': 'Номер стола',
            'status': 'Статус заказа'
        }
        widgets: Dict[str, Any] = {
            'table_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class OrderItemForm(forms.ModelForm):
    """
    Класс добавления элемента (блюда) в заказ.

    Поля:
        menu_item - выбор блюда из списка (выпадающий список);
        quantity - количество (минимум 1) (числовое поле).
    """

    menu_item = forms.ModelChoiceField(
        queryset=MenuItem.objects.all(),
        label='Блюдо',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    quantity = forms.IntegerField(
        label='Количество',
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model: Model = OrderItem
        fields: List[str] = ['menu_item', 'quantity']

    def save(self, commit=True, order=None):
        """
        Функция сохранения заказа.

        :param commit: оператор подтверждения транзакции (True - сразу сохранить, False - отложить сохранение).
        :param order: объект текущего заказа.
        :return:
        """
        if order is None:
            raise ValueError("Order must be provided")
        instance: OrderItem = super().save(commit=False)
        instance.order = order
        instance.price = instance.menu_item.price * instance.quantity
        if commit:
            instance.save()
        return instance


class MenuItemViewSet(viewsets.ModelViewSet):
    """
    Класс CRUD API для блюд Меню.

    Права доступа:
        Чтение - доступно всем
        Изменение - только авторизованным пользователям
    """

    queryset: QuerySet[MenuItem] = MenuItem.objects.all()
    serializer_class: ModelSerializer = MenuItemSerializer
    permission_classes: List[BasePermission] = [permissions.IsAuthenticatedOrReadOnly]


class MenuItemForm(forms.ModelForm):
    """
    Класс управления блюдами Меню.

    Поля:
        name - название блюда (текстовое поле);
        price - цена за 1 ед. блюда (минимум 0) (числовое поле с шагом 0.01).
    """

    class Meta:
        model: Model = MenuItem
        fields: List[str] = ['name', 'price']
        widgets: Dict[str, Any] = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
        }


class OrderViewSet(viewsets.ModelViewSet):
    """
    Класс управление заказами через API.

    Права доступа:
        Чтение и изменение - только авторизованным пользователям
    """

    queryset: QuerySet[Order] = Order.objects.all().order_by('-created_at')
    serializer_class = OrderListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        """
        Функция получения списка заказов, согласно параметрам
        фильтрации ('table' - номер стола, 'status' - статус заказа).

        :return: список объектов заказа
        """

        queryset: QuerySet[Order] = super().get_queryset()
        table_number: int = self.request.query_params.get('table')
        status: str = self.request.query_params.get('status')

        if table_number:
            queryset = queryset.filter(table_number=table_number)
        if status:
            queryset = queryset.filter(status=status)

        return queryset
