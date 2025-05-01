from django.db import models
from apps.models import BaseModel
from auth_user.models import User
from apps.geo.models import Region
import re 

class Color(BaseModel):
    name = models.CharField(max_length=200, blank=True, null=True)
    code = models.CharField(max_length=50, default='#ffff')
    class Meta:
        db_table = "colors"

    def __str__(self) -> str:
        return self.name

        
class Product(BaseModel):
    name = models.CharField(max_length=200, blank=True, null=True)
    amount = models.BigIntegerField(default=0)
    pack = models.BigIntegerField(default=0)
    color = models.ManyToManyField(Color)
    type = models.CharField(max_length=20, choices=[('is_active', 'Active'), ('is_disabled', 'Disabled')])
    ordering = models.BigIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = "products"
        ordering = ['ordering']
        
    def __str__(self) -> str:
        return self.name
    
        
class CategoryMeterial(BaseModel):
    name = models.CharField(max_length=200, blank=True, null=True)
    class Meta:
        db_table = 'category_meterial'
    
    def __str__(self) -> str:
        return self.name

class Meterial(BaseModel):
    category = models.ForeignKey(CategoryMeterial, on_delete=models.CASCADE, related_name="stocks_list")
    name = models.CharField(max_length=200, blank=True, null=True)
    amount = models.BigIntegerField(default=0)
    
    class Meta:
        db_table = 'meterials'
    
    def __str__(self) -> str:
        return self.name
    
class QuantityChangeMeterial(BaseModel):
    meterial = models.ForeignKey(Meterial, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    change_type = models.CharField(max_length=10, choices=[('add', 'Добавлять'), ('subtract', 'Вычесть')])
    type = models.CharField(max_length=10, choices=[('amount', 'Количество'), ('defect', 'Дефект')])
    quantity_changed = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user} - {self.change_type} {self.quantity_changed} of {self.product.name}"
    

class ProductionProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    class Meta:
        db_table = "production_products"
        
    def __str__(self) -> str:
        return f"{self.product}"

 
class ProductColorQuantity(models.Model):
    product = models.ForeignKey(ProductionProduct, on_delete=models.CASCADE, related_name='product_color_quantity')
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    quantity = models.BigIntegerField(default=0)
    weight = models.BigIntegerField(default=0)
    packaging = models.BigIntegerField(default=0)
    
    class Meta:
        db_table = "product_color_quantities"
        ordering = ['-id']
        
    def __str__(self) -> str:
        return f"{self.product.product.name} - {self.color.name}"
    
class QuantityChange(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    user = models.CharField(max_length=50, blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, blank=True, null=True)
    change_type = models.CharField(max_length=10, choices=[('add', 'Добавлять'), ('subtract', 'Вычесть')])
    type = models.CharField(max_length=10, choices=[('amount', 'Количество'), ('defect', 'Дефект')])
    quantity_changed = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user} - {self.change_type} {self.quantity_changed} of {self.product.name}"