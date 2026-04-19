import uuid  # Для унікального номера
from django.db import models
from django.contrib.auth.models import User
from shop.models import Product


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'В очікуванні'),
        ('paid', 'Оплачено'),
        ('shipped', 'Відправлено'),
        ('cancelled', 'Скасовано'),
    )

    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE, verbose_name="Користувач")


    order_number = models.CharField(max_length=20, unique=True, editable=False)

    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=5)
    city = models.CharField(max_length=100)

    # 2. Дата створення
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']

    def save(self, *args, **kwargs):
        if not self.order_number:

            self.order_number = str(uuid.uuid4().hex[:10]).upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_number}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.id}"

    def get_cost(self):
        return self.price * self.quantity

