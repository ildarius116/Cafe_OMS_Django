from rest_framework import serializers
from django.db.models import Model
from typing import List, Dict, Any
from .models import Order, MenuItem, OrderItem


class MenuItemSerializer(serializers.ModelSerializer):
    """
    Сериализатор элементов (блюда) Меню.

    Поля:
        id - автоматически создаваемый идентификатор;
        name - название блюда;
        price - цена блюда.
    """

    class Meta:
        model: Model = MenuItem
        fields: List[str] = ['id', 'name', 'price']


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Сериализатор 1 элемента (блюда) Меню в заказе.

    Поля:
        menu_item - блюда из меню (обязательный элемент);
        quantity - количество блюд (минимальное количество - 1);
        price - суммарная цена блюда.
    """

    class Meta:
        model: Model = OrderItem
        fields: List[str] = ['id', 'menu_item', 'quantity', 'price']
        read_only_fields: List[str] = ['price']
        extra_kwargs: Dict[str, Dict[str, Any]] = {'menu_item': {'required': True}, 'quantity': {'min_value': 1}}


class OrderCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор создания заказа.

    Поля:
        table_number - номер стола;
        status - статус заказа;
        items - вложенные позиции (блюда) заказа;
    """

    items = OrderItemSerializer(many=True, source='order_items')

    class Meta:
        model = Order
        fields: List[str] = ['id', 'table_number', 'status', 'items']

    def create(self, validated_data) -> Order:
        """
        Функция создания заказа.

        :param validated_data: валидированные данные заказа.
        :return: объект заказа.
        """

        # извлечение данных об элементах (блюдах) заказа
        items_data = validated_data.pop('order_items')
        # создание объекта заказа
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            menu_item = item_data['menu_item']
            # наполнение заказа элементами (блюдами) заказа
            OrderItem.objects.create(
                order=order,
                menu_item=menu_item,
                quantity=item_data['quantity'],
                price=menu_item.price * item_data['quantity']
            )
        # расчет итоговой цены заказа
        order.total_price = order.calculate_total()
        order.save()
        return order


class OrderListSerializer(serializers.ModelSerializer):
    """
    Сериализатор выдачи списка заказов.

    Поля:
        table_number - номер стола;
        status - статус заказа;
        items - вложенные позиции (блюда) заказа;
        total_price - итоговая цена всех блюд (только для чтения).
    """

    items = OrderItemSerializer(many=True, source='order_items', read_only=True)

    class Meta:
        model = Order
        fields: List[str] = ['id', 'table_number', 'status', 'total_price', 'items']
