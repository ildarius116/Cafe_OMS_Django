from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.db.models.query import QuerySet
from typing import Optional
from .models import Order, OrderItem
from .forms import OrderForm, OrderItemForm, MenuItemForm


class OrderListView(View):
    """Класс отображения списка заказов"""

    def get(self, request) -> render:
        """
        Функция получения списка заказов.
        :param request:
        :return: html-страница списка заказов.
        """
        orders: QuerySet[Order] = Order.objects.all().order_by('-created_at')

        # попытка получить параметры фильтрации из request (адресной строки)
        table_number: Optional[str] = request.GET.get('table')
        status: Optional[str] = request.GET.get('status')

        # фильтрация, при наличии параметров фильтрации
        if table_number:
            orders = orders.filter(table_number=table_number)
        if status:
            orders = orders.filter(status=status)

        return render(request, 'cafe/order_list.html', {
            'orders': orders,
            'current_table': table_number,
            'current_status': status
        })


class OrderCreateView(View):
    """Класс создания заказа"""

    def get(self, request) -> render:
        """
        Функция обработки Get-запроса.
        :param request:
        :return: html-страница (формы) создания заказа.
        """
        form = OrderForm()
        return render(request, 'cafe/order_form.html', {'form': form})

    def post(self, request) -> (redirect, render):
        """
        Функция обработки POST-запроса.
        :param request:
        :return: html-страница создания заказа, при получении невалидных данных.
                 html-страница отображения деталей текущего заказа, при получении валидных данных.
        """
        form = OrderForm(request.POST)
        if form.is_valid():
            order: Order = form.save(commit=False)
            order.save()
            return redirect('order_detail', pk=order.pk)
        return render(request, 'cafe/order_form.html', {'form': form})


class OrderDetailView(View):
    """Класс детализации заказа"""

    def get(self, request, pk) -> render:
        """
        Функция обработки Get-запроса.
        :param request:
        :param pk: id - заказа
        :return: html-страница отображения детализации конкретного (pk) заказа.
        """
        order: Order = get_object_or_404(Order, pk=pk)
        item_form = OrderItemForm()
        return render(request, 'cafe/order_detail.html', {
            'order': order,
            'item_form': item_form
        })


class OrderUpdateView(View):
    """Класс обновления статуса заказа"""

    def get(self, request, pk) -> render:
        """
        Функция обработки Get-запроса.
        :param request:
        :param pk: id - заказа
        :return: html-страница редактирования статуса конкретного (pk) заказа.
        """
        order: Order = get_object_or_404(Order, pk=pk)
        form = OrderForm(instance=order)
        return render(request, 'cafe/order_form.html', {'form': form})

    def post(self, request, pk) -> (redirect, render):
        """
        Функция обработки POST-запроса.
        :param request:
        :param pk: id - заказа
        :return: html-страница редактирования статуса конкретного (pk) заказа, при получении невалидных данных.
                 html-страница отображения деталей конкретного (pk) заказа, при получении валидных данных.
        """
        order: Order = get_object_or_404(Order, pk=pk)
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_detail', pk=order.pk)
        return render(request, 'cafe/order_form.html', {'form': form})


class OrderDeleteView(View):
    """Класс удаления заказа"""

    def post(self, request, pk) -> redirect:
        """
        Функция обработки POST-запроса.
        :param request:
        :param pk: id - заказа
        :return: перенаправление на html-страницу списка заказов.
        """
        order: Order = get_object_or_404(Order, pk=pk)
        order.delete()
        return redirect('order_list')


class RevenueReportView(View):
    """Класс отображения отчет о выручке"""

    def get(self, request) -> render:
        """
        Функция обработки Get-запроса.
        :param request:
        :return: html-страница отображения отчета о выручке.
        """
        # получение заказов со статусом "оплачено"
        paid_orders: QuerySet[Order] = Order.objects.filter(status='paid')
        total_revenue: float = sum(order.total_price for order in paid_orders)
        return render(request, 'cafe/revenue_report.html', {
            'paid_orders': paid_orders,
            'total_revenue': total_revenue
        })


class MenuItemCreateView(View):
    """Класс создания (добавления) блюда (в меню)"""

    def get(self, request) -> render:
        """
        Функция обработки Get-запроса.
        :param request:
        :return: html-страница (формы) создания блюда.
        """
        form = MenuItemForm()
        return render(request, 'cafe/menu_item_form.html', {'form': form})

    def post(self, request) -> (redirect, render):
        """
        Функция обработки POST-запроса.
        :param request:
        :return: html-страница (формы) создания блюда, при получении невалидных данных.
        """
        form = MenuItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Блюдо успешно добавлено!')
            return redirect('menu_item_create')

        return render(request, 'cafe/menu_item_form.html', {'form': form})


class AddOrderItemView(View):
    """Класс добавления блюда в заказ"""

    def post(self, request, pk) -> redirect:
        """
        Функция обработки POST-запроса.
        :param request:
        :param pk: id - текущего заказа
        :return: html-страница отображения деталей текущего заказа.
        """
        order: Order = get_object_or_404(Order, pk=pk)
        form = OrderItemForm(request.POST)

        if form.is_valid():
            form.save(order=order)
            messages.success(request, 'Блюдо успешно добавлено в заказ!')
        else:
            messages.error(request, 'Ошибка при добавлении блюда')

        return redirect('order_detail', pk=order.pk)


class DeleteOrderItemView(View):
    """Класс удаления блюда из заказа"""

    def post(self, request, pk) -> redirect:
        """
        Функция обработки POST-запроса.
        :param request:
        :param pk: id - текущего заказа
        :return: html-страница отображения деталей текущего заказа.
        """
        item = get_object_or_404(OrderItem, pk=pk)
        order_pk = item.order.pk
        item.delete()
        messages.success(request, 'Блюдо удалено из заказа')
        return redirect('order_detail', pk=order_pk)
