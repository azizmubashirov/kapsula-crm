from typing import Any
from django import forms
from .models import Client, Contact, UserCategory
from apps.geo.models import District, Region
from django.forms import inlineformset_factory
from apps.product.models import Product

class UserForm(forms.ModelForm):
    # other_product = forms.CharField(
    #     widget=forms.TextInput(attrs={
    #         "class": "form-control my-4", 
    #         'id': 'TagifyBasic', 
    #         'placeholder': 'Другие продукты'
    #         }),
    #         required=False 
    #     )
    class Meta:
        model = Client
        fields = "__all__"
        
        labels = {
                "name": "Название компании",
                "region": "Область",
                "district": "Районы",
                "comment": "Комментарий",
                "product": "Продукт",
                "category": "Категория",
            }
        
        widgets = {
                "name": forms.TextInput(attrs={"class": "form-control"}),
                "region": forms.Select(attrs={"class": "form-control"}),
                "district": forms.Select(attrs={"class": "form-control"}),
                "category": forms.SelectMultiple(attrs={"class": "selectpicker w-100", 'multiple': True, 'data-actions-box': True, 'id': 'selectpickerSelectDeselect', 'data-style': 'btn-default'}),
                "product": forms.SelectMultiple(attrs={"class": "selectpicker w-100", 'multiple': True, 'data-actions-box': True, 'id': 'selectpickerSelectDeselect', 'data-style': 'btn-default'}),
                "comment": forms.Textarea(attrs={"class": "form-control", 'rows': 8}),
            }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = UserCategory.objects.order_by('name')
        self.fields['region'].queryset = Region.objects.order_by('name_uz')
        self.fields['product'].queryset = Product.objects.order_by('ordering')
        if self.instance.region:
                self.fields['district'] = forms.ModelChoiceField(
                queryset=District.objects.filter(region_id=self.instance.region.id).order_by('name_uz'),
                label="Районы",
                required=True,
                widget=forms.Select(attrs={'class': 'form-control'})
            )
        elif self.instance.pk:
            self.fields['district'].choices = []
    
    # def save(self, commit=True):
    #     client = super().save(commit=False)

    #     # other_products = self.cleaned_data.get('other_product', '')
    #     # product_names = [name.strip() for name in other_products.split(',') if name.strip()]

    #     # product_ids = []
    #     # for product_name in product_names:
    #         # product, created = Product.objects.get_or_create(name=product_name)
    #         # product_ids.append(product.id)

    #     if commit:
    #         client.save()
    #         # client.product.set(product_ids)
    #     return client
    
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'phone_number', 'position']
        labels = {
                "name": "Имя",
                "phone_number": "Номер телефона",
                "position": "Позиция",
            }
        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control"}),
            'phone_number': forms.TextInput(attrs={"class": "form-control"}),
            'position': forms.TextInput(attrs={"class": "form-control"}),
        }
    def clean(self):
        cleaned_data = super().clean()
        if not self.instance.pk:
            if 'id' in cleaned_data and not cleaned_data['id']:
                del cleaned_data['id']
        return cleaned_data
        

# ContactFormSet = inlineformset_factory(
#     Client,
#     Contact,
#     form=ContactForm,
#     extra=2,
#     can_delete=True,
#     validate_min=False,
#     validate_max=False,
#     fields=['id', 'name', 'phone_number']
# )
ContactFormSet = ""