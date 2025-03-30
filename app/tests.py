from django.test import TestCase, Client
from django.urls import reverse

from .models import Order, MenuItem, OrderItem

items_dict = {
    "Кофе": 60.00,
    "Чай": 10.00,
    "Суп": 20.00,
    "Бутик": 15.00,
}

items_tuple = (("Кофе", 60.00),
               ("Чай", 10.00),
               ("Суп", 20.00),
               ("Бутик", 15.00),
               )


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


class OrderModelTest(TestCase):
    def setUp(self):
        self.menu_item_1 = MenuItem.objects.create(name="Кофе", price=5.00)
        self.menu_item_2 = MenuItem.objects.create(name="Чай", price=3.00)
        self.order = Order.objects.create(table_number=1)

    def test_order_total_calculation_one_item(self):
        """Тест корректности создания заказа с одним блюдом"""

        create_order_item(self.order, self.menu_item_1, 2)
        self.order.refresh_from_db()
        self.assertEqual(self.order.total_price, 10.00)

    def test_order_total_calculation_multy_items(self):
        """Тест корректности создания заказа с несколькими блюдами"""

        create_order_item(self.order, self.menu_item_1, 2)
        create_order_item(self.order, self.menu_item_2, 3)
        self.order.refresh_from_db()
        self.assertEqual(self.order.total_price, 19.00)

    def tearDown(self):
        Order.objects.all().delete()
        MenuItem.objects.all().delete()


class OrderViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.order = Order.objects.create(table_number=2)

    def test_order_list_view(self):
        """Тест доступности страницы со списком заказов"""

        response = self.client.get(reverse('order_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, ">2</td>")
        self.assertContains(response, "<td>0,00 ₽</td>")

    def test_order_list_view_with_orders(self):
        """Тест правильного отображения списка заказов"""

        self.menu_item = MenuItem.objects.create(name="Чай", price=3.00)
        create_order_item(self.order, self.menu_item, 3)
        self.menu_item = MenuItem.objects.create(name="Бутик", price=15.00)
        create_order_item(self.order, self.menu_item, 2)
        response = self.client.get(reverse('order_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, ">2</td>")
        self.assertContains(response, "<li>3 × Чай - 9,00 ₽</li>")
        self.assertContains(response, "<li>2 × Бутик - 30,00 ₽</li>")
        self.assertContains(response, "<td>39,00 ₽</td>")

    def test_order_create_view(self):
        """Тест функционала (перехода на страницу) создания заказа"""

        response = self.client.post('/new/', {
            'table_number': 3,
            'status': 'pending'
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.count(), 2)

    def tearDown(self):
        Order.objects.all().delete()
        MenuItem.objects.all().delete()


class OrderUpdateTest(TestCase):
    def setUp(self):
        self.menu_item = MenuItem.objects.create(name="Суп", price=10.00)
        self.order = Order.objects.create(table_number=3)

    def test_order_total_updates(self):
        """Тест полного обновления заказа"""

        self.assertEqual(self.order.total_price, 0.00)  # 0.00 * 0 = 0.00

        create_order_item(self.order, self.menu_item, 2)
        self.order.refresh_from_db()
        self.assertEqual(self.order.total_price, 20.00)  # 10.00 * 2 = 20.00

    def test_order_update_quantity(self):
        """Тест изменения количества элементов (блюд) в заказе"""

        order_item = create_order_item(self.order, self.menu_item, 1)
        self.order.refresh_from_db()
        self.assertEqual(self.order.total_price, 10.00)

        order_item.quantity = 3
        order_item.save()
        self.order.refresh_from_db()
        self.assertEqual(self.order.total_price, 30.00)

    def tearDown(self):
        Order.objects.all().delete()
        MenuItem.objects.all().delete()
