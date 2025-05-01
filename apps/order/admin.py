
from django.contrib import admin
from .models import Order, OrderCLient, OrderYearFolder, OrderPayment

admin.site.register(Order)
admin.site.register(OrderCLient)
admin.site.register(OrderYearFolder)
admin.site.register(OrderPayment)