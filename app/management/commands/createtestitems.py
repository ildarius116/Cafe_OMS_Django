import logging
from random import randint, choice
from django.core.management.base import BaseCommand
from ...models import Order, MenuItem, OrderItem

logger = logging.Logger(__name__)


def create_order_item(order, menu_item, quantity):
    """
    Функция-шаблон создания элемента заказа.

    :param order: объект заказа
    :param menu_item: объект элемента (блюда) Меню
    :param quantity: количество элементов в заказе
    :return: объект элемента заказа
    """
    order_item = OrderItem.objects.create(
        order=order,
        menu_item=menu_item,
        quantity=quantity
    )
    return order_item


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Функция обработчик команды.
        Создает рандомные тестовые заказы и блюда в меню.
        """

        items_dict = {
            "Кофе": 60.00,
            "Чай": 10.00,
            "Компот": 10.00,
            "Суп": 20.00,
            "Сендвич": 35.00,
            "Яичница": 15.00,
        }

        for i in range(1, 6):
            # случайный номер стола
            table_number = randint(1, 10)
            # создание заказа
            order = Order.objects.create(table_number=table_number)
            # создание копии словаря блюд
            items = items_dict.copy()
            # случайное количество блюд в заказе
            order_items = randint(1, 5)
            for j in range(order_items):
                # случайный выбор блюда из меню
                menu_random = choice(list(items.keys()))
                # создание объекта меню
                menu_item = MenuItem.objects.create(name=menu_random, price=items_dict[menu_random])
                # удаление выбранного блюда из словаря, чтобы не повторялось
                items.pop(menu_random)
                # случайное количество заказанного блюда
                quantity = randint(1, 5)
                # создание элемента заказа
                order_item = create_order_item(order, menu_item, quantity)
                logger.info(f"created Order-item: {order_item} and Table: {table_number}")
                print(f"created Order-item: {order_item} and Table: {table_number}")

