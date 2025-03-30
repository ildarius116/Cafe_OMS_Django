from datetime import datetime
from django.db import models
from django.db.models.query import QuerySet
from typing import List


class MenuItem(models.Model):
    name: str = models.CharField(max_length=100, verbose_name='Название блюда')
    price: float = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='Цена'
    )

    def __str__(self):
        return f"{self.name} - {self.price}₽"

    class Meta:
        verbose_name: str = 'Блюдо'
        verbose_name_plural: str = 'Блюда'


class Order(models.Model):
    STATUS_CHOICES: List[tuple] = [
        ('pending', 'В ожидании'),
        ('ready', 'Готово'),
        ('paid', 'Оплачено'),
    ]

    table_number: int = models.PositiveIntegerField()
    items: QuerySet[MenuItem] = models.ManyToManyField(MenuItem, through='OrderItem')
    total_price: float = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status: str = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at: datetime = models.DateTimeField(auto_now_add=True)
    updated_at: datetime = models.DateTimeField(auto_now=True)

    def calculate_total(self):
        if not self.pk:
            return 0
        return sum(item.price for item in self.order_items.all())

    def save(self, *args, **kwargs):
        if not self.pk:
            return super().save(*args, **kwargs)
        super().save(*args, **kwargs)
        self.total_price = self.calculate_total()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.id} - Table {self.table_number}"


class OrderItem(models.Model):
    order: Order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    menu_item: MenuItem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity: int = models.PositiveIntegerField(default=1)
    price: float = models.DecimalField(max_digits=8, decimal_places=2)

    def save(self, *args, **kwargs):
        self.price = self.menu_item.price * self.quantity
        super().save(*args, **kwargs)
        self.order.save()

    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name} for Order #{self.order.id}"
