from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('cage', 'Cage & Carriers'),
        ('identification', 'Identification Belts & Tags'),
        ('book', 'Pet Care Books'),
        ('food', 'Pet Food & Treats'),
        ('rope', 'Ropes & Leashes'),
        ('brush', 'Grooming Brushes'),
        ('nail_cutter', 'Nail Cutters & Trimmers'),
        ('soap', 'Pet Soaps'),
        ('shampoo', 'Pet Shampoos'),
        ('other', 'Other Accessories'),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text='Price in BDT')
    quantity = models.PositiveIntegerField(default=0, help_text='Available stock quantity')
    image = models.ImageField(upload_to='store/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return f'{self.name} (Stock: {self.quantity})'

    @property
    def is_in_stock(self):
        return self.quantity > 0


class Order(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cod', 'Cash on Delivery'),
        ('online', 'Online Payment (Dummy)'),
    ]
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending Payment'),
        ('paid', 'Paid'),
    ]
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='store_orders')
    full_name = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=20)
    shipping_address = models.TextField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cod')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='confirmed')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Order #{self.pk} by {self.user.username} (BDT {self.total_amount})'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items')
    product_name = models.CharField(max_length=200, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.quantity}x {self.product_name or self.product.name} (Order #{self.order.pk})'

    @property
    def subtotal(self):
        return self.price_at_purchase * self.quantity

    def save(self, *args, **kwargs):
        if not self.product_name and self.product:
            self.product_name = self.product.name
        super().save(*args, **kwargs)

