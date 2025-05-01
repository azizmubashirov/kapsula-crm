from django.db import models
from apps.models import BaseModel
from apps.geo.models import Region, District
from apps.product.models import Product


class UserCategory(BaseModel):
    name = models.CharField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        return self.name or '-----'
    
    class Meta:
        ordering = ['name']

class Client(BaseModel):
    name = models.CharField(max_length=200, blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL,
                               blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL,
                                 blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    product = models.ManyToManyField(Product, related_name='client_products')
    category = models.ManyToManyField(UserCategory, related_name='client_categories')
    
    class Meta:
        db_table = 'clients'
    
    def __str__(self) -> str:
        return self.name if self.name else "Unnamed Client"
    
class Contact(BaseModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='client_contacts')
    name = models.CharField(max_length=200, blank=True, null=True)
    phone_number = models.CharField(max_length=200, blank=True, null=True)
    position = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'contacts'
        
    def __str__(self) -> str:
        return str(self.name) + " " + str(self.phone_number) or self.id
