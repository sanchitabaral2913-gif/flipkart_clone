# orders/models.py
from django.db import models
from accounts.models import User
from products.models import Product

# ---------------------------
# Cart Model
# ---------------------------
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} x {self.quantity}"

    def total_price(self):
        return self.product.price * self.quantity

# ---------------------------
# Order Model
# ---------------------------
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    ]

    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)  # ✅ automatic date & time

    
    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

# ---------------------------
# Order Item Model
# ---------------------------
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.FloatField()  # ensure ye line models.py me hai



    def subtotal(self):
        return self.price * self.quantity
