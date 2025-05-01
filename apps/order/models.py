from django.db import models
from apps.models import BaseModel
from apps.product.models import ProductColorQuantity, Color
from apps.users.models import Client
from apps.product.models import Product
from decimal import Decimal
from apps.geo.models import Region, District
from django.utils import timezone


class OrderCLient(BaseModel):
    name = models.CharField(max_length=200, blank=True, null=True)
    phone_number = models.CharField(max_length=200, blank=True, null=True)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL,
                               blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL,
                                 blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    product = models.ManyToManyField(Product, related_name='order_client_products')
    
    
    def __str__(self) -> str:
        return self.name + " " + self.phone_number if self.name else "Unnamed Client"

class OrderYearFolder(BaseModel):
    folder = models.ForeignKey(OrderCLient, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self) -> str:
        return self.name

class Order(BaseModel):
    product = models.CharField(max_length=100, blank=True, default='')
    color = models.CharField(max_length=100, blank=True, null=True)
    color_obj = models.ForeignKey(Color, on_delete=models.SET_NULL,
                                  blank=True, null=True)
    client = models.ForeignKey(OrderCLient,
                               on_delete=models.CASCADE,
                               blank=True, null=True)
    year = models.CharField(max_length=100, blank=True, default='')
    count = models.BigIntegerField(default=0)
    price = models.DecimalField(max_digits=12, decimal_places=10, default=0.0)
    total_price_order = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    remainder = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)
    created_date = models.DateField(default=timezone.now)
    
    class Meta:
        db_table = 'orders'
    
    def total_price(self):
        return self.total_price_order if self.total_price_order else  Decimal(self.count) * self.price
    
    def __str__(self):
        return "%s - %s - %s" %(self.product, self.client, self.count)
    
class OrderPayment(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_payments")
    paid_price = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)
    paid_price_sum = models.BigIntegerField(default=0)
    comment = models.TextField(blank=True, null=True)
        