from typing import Any
from django import forms
from .models import Order, OrderCLient
from apps.product.models import ProductColorQuantity, Color
from apps.users.models import Client
from apps.geo.models import District
from decimal import Decimal
from apps.geo.models import Region
from datetime import datetime

class OrderForm(forms.ModelForm):
    paid_amount = forms.CharField(required=False)
    paid_amount_sum = forms.CharField(required=False)
    remainder = forms.CharField(required=False)
    comment = forms.CharField(required=False)
    created_date = forms.CharField(required=False)
    color_obj = forms.ModelChoiceField(queryset=Color.objects.all(), required=False)
    count = forms.CharField(required=False)
    total_price_order = forms.CharField(required=False)
    price = forms.CharField(required=False)
    class Meta:
        model = Order
        fields = ['product', 'client', 'price', 'paid_amount',  'total_price_order',
                  'count', 'remainder', 'paid_amount_sum', 'created_date',
                  'color_obj', 'comment', 'year']
    
    def clean_remainder(self):
        cleaned_data = self.cleaned_data
        total_price = cleaned_data.get('total_price_order') if not cleaned_data.get('total_price_order') == '' else 0
        remainder =  round(Decimal(total_price) - Decimal(cleaned_data.get('paid_amount') or 0), 2)
        return remainder
        
    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['year'] = self.instance.year
        try:
            cleaned_data['created_date'] = datetime.strptime(cleaned_data['created_date'] + f"/{cleaned_data['year']}", "%d/%m/%Y").date()
        except ValueError:
            cleaned_data['created_date'] = datetime.now()
        cleaned_data = {k: v for k, v in cleaned_data.items() if v not in [None, '', []]}
        return cleaned_data
    
    def get_label_from_instance(self, obj):
        return f"{obj.product.product.name} - {obj.color.name}"

class EditOrderForm(forms.ModelForm):
    paid_amount = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Оплата"
        )
    paid_amount_sum = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Оплата (сум)"
        )
    class Meta:
        model = Order
        fields = ['product', 'price', 'paid_amount', 'count', 'paid_amount_sum', 'created_date', 'color_obj']
        labels = {
                "product": "Грамм",
                "client": "Клиент",
                "price": "Цена",
            }
        
class OrderClientForm(forms.ModelForm):
    
    class Meta:
        model = OrderCLient
        fields = ('name', 'region', 'district', 'comment', 'phone_number', 'product', 'first_name')
        
        labels = {
                "name": "Название",
                "region": "Область",
                "district": "Районы",
                "comment": "Комментарий",
                "phone_number": "Номер телефона",
                "first_name": "Имя",
                "product": "Продукт",
            }
        
        widgets = {
                "name": forms.TextInput(attrs={"class": "form-control"}),
                "region": forms.Select(attrs={"class": "form-control"}),
                "district": forms.Select(attrs={"class": "form-control"}),
                "comment": forms.Textarea(attrs={"class": "form-control"}),
                "phone_number": forms.TextInput(attrs={"class": "form-control"}),
                "first_name": forms.TextInput(attrs={"class": "form-control"}),
                "product": forms.SelectMultiple(attrs={"class": "selectpicker w-100", 'multiple': True, 'data-actions-box': True, 'id': 'selectpickerSelectDeselect', 'data-style': 'btn-default'}),
            }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.region:
                self.fields['district'] = forms.ModelChoiceField(
                queryset=District.objects.filter(region_id=self.instance.region.id),
                label="Районы",
                required=True,
                widget=forms.Select(attrs={'class': 'form-control'})
            )
        elif self.instance.pk:
            self.fields['district'].choices = []
            

class ProductionProductForm(forms.Form):
    
    quantity = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Количество"
        )
    user = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Организация"
        )
    
    region = forms.ModelChoiceField(
        queryset=Region.objects.order_by('name_uz'),
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Область"
    )