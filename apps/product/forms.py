
from typing import Any
from django import forms
from .models import (
    Product, 
    Color, 
    Meterial, 
    ProductColorQuantity, 
    ProductionProduct,
    CategoryMeterial
    )
from apps.users.models import UserCategory
from django.forms.widgets import TextInput
from django.forms import inlineformset_factory
import re 

class ColorInput(TextInput):
    input_type = 'color'
    
    
class ProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        fields = ('name', 'color', 'is_active')
        
        labels = {
                "name": "Название",
                "color": "Выберите цвета",
                "is_active": "активен",
            }
        
        widgets = {
                "name": forms.TextInput(attrs={"class": "form-control"}),
                "is_active": forms.CheckboxInput(attrs={"class": "form-check"}),
                "color": forms.SelectMultiple(attrs={"class": "selectpicker w-100", 'multiple': True, 'data-actions-box': True, 'id': 'selectpickerSelectDeselect', 'data-style': 'btn-default'}),
            }
    
    def save(self, commit=True, *args, **kwargs):
        from django.db import transaction
        with transaction.atomic():
            model = super().save(commit=True)
            matches = re.findall(r"(\d+)\s*(gr|litr|гр|литр)", model.name)
            if matches:
                model.ordering = int(matches[0][0])
            if commit:
                model.save()
                
            if model.is_active:
                production_product, created = ProductionProduct.objects.get_or_create(product=model)
            
                current_colors = set(model.color.values_list('id', flat=True))
                existing_colors = set(production_product.product_color_quantity.values_list('color_id', flat=True))
                
                colors_to_add = current_colors - existing_colors
                for color_id in colors_to_add:
                    color = Color.objects.get(id=color_id)
                    ProductColorQuantity.objects.create(
                        product=production_product,
                        color=color
                    )
                
                colors_to_delete = existing_colors - current_colors
                for color_id in colors_to_delete:
                    ProductColorQuantity.objects.filter(
                        product=production_product,
                        color_id=color_id
                    ).delete()
            return model

class ColorForm(forms.ModelForm):
    class Meta:
        model = Color
        fields = ('name', 'code')
        
        labels = {
                "name": "Название",
                'code': 'Цветовой код'
            }
        widgets = {
                "name": forms.TextInput(attrs={"class": "form-control"})
            }

class UserCategoryForm(forms.ModelForm):
    class Meta:
        model = UserCategory
        fields = ('name', )
        
        labels = {
                "name": "Название",
            }
        widgets = {
                "name": forms.TextInput(attrs={"class": "form-control"})
            }
        
class CategoryMeterialForm(forms.ModelForm):
    class Meta:
        model = CategoryMeterial
        fields = ('name',)
        labels = {
                "name": "Название",
            }
        widgets = {
                "name": forms.TextInput(attrs={"class": "form-control"})
            }

class SkladForm(forms.ModelForm):
    class Meta:
        model = Meterial
        fields = ('name', 'amount')
        labels = {
                "name": "Название",
                "amount": "Количество",
            }
        widgets = {
                "name": forms.TextInput(attrs={"class": "form-control"}),
                "amount": forms.NumberInput(attrs={"class": "form-control"}),
            }
        
    
MeterialFormSet = inlineformset_factory(
    CategoryMeterial,
    Meterial, 
    form=SkladForm, 
    extra=5,
    can_delete=True
)