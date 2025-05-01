from django.views.generic import TemplateView, UpdateView, DeleteView, DetailView
from web_project import TemplateLayout
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Product, Color, Meterial, CategoryMeterial
from django.core.paginator import Paginator
from apps.users.models import UserCategory
from .forms import ProductForm, ColorForm, SkladForm, CategoryMeterialForm, MeterialFormSet, UserCategoryForm
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.db.models import Q
from django.db import transaction

class ProductsView(TemplateView):
    
    form_class = ProductForm
    success_url = reverse_lazy('app-product-list')

    def get_context_data(self, **kwargs):
        search_query = self.request.GET.get('q', '')
        page_number = int(self.request.GET.get('page', 1))
        entries = int(self.request.GET.get("entries", 25))
        
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        
        products =  Product.objects.order_by('ordering')
        context['form'] = self.form_class()
        if search_query:
            products = products.filter(name__icontains=search_query)
        paginator = Paginator(products, entries)
        
        context['items'] = paginator.page(page_number)
        context['search_query'] = search_query
        context['entries'] = entries
        context['entries_list'] = [5,25,50,100,200]
        context['type'] = 'product'

        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect(self.success_url)
        else:
            print("Main Form Errors:", form.errors)
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('app-product-list')
    
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context
    
def delete_product(request, pk):
    product = Product.objects.get(pk=pk)
    product.delete()
    return redirect(reverse_lazy('app-product-list'))


class ColorsView(TemplateView):
    form_class = ColorForm
    success_url = reverse_lazy('app-color-list')

    def get_context_data(self, **kwargs):
        search_query = self.request.GET.get('q', '')
        page_number = int(self.request.GET.get('page', 1))
        entries = int(self.request.GET.get("entries", 25))
        
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        
        colors =  Color.objects.order_by('name')
        context['form'] = self.form_class()
        if search_query:
            colors = colors.filter(name__icontains=search_query)
        paginator = Paginator(colors, entries)
        
        context['items'] = paginator.page(page_number)
        context['search_query'] = search_query
        context['entries'] = entries
        context['entries_list'] = [5,25,50,100,200]
        context['type'] = 'color'

        return context
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect(self.success_url)
        else:
            print("Main Form Errors:", form.errors)
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)

class ColorUpdateView(UpdateView):
    model = Color
    form_class = ColorForm
    success_url = reverse_lazy('app-color-list')
    
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['type'] = 'color'
        return context
    
def delete_color(request, pk):
    color = Color.objects.get(pk=pk)
    color.delete()
    return redirect(reverse_lazy('app-color-list'))

class SkladView(TemplateView):
    form_class = CategoryMeterialForm
    success_url = reverse_lazy('app-sklad-list')
    
    def get_context_data(self, **kwargs):
        entries = int(self.request.GET.get("entries", 25))
        page_number = int(self.request.GET.get('page', 1))
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        
        paginator = Paginator(CategoryMeterial.objects.all().order_by('name'), entries)
        context['items'] = paginator.page(page_number)
        
        context['form'] = self.form_class
        context['formset'] = MeterialFormSet(instance=CategoryMeterial())
        context['entries'] = entries
        context['entries_list'] = [5,25,50,100,200]
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        formset = MeterialFormSet(request.POST, instance=CategoryMeterial())

        if form.is_valid() and formset.is_valid():
            category = form.save()
            formset.instance = category
            formset.save()
            return redirect(self.success_url)
        else:
            print("Main Form Errors:", form.errors)
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)
    
def sklad_edit(request, pk):
    if request.POST:
        data = request.POST
        with transaction.atomic():
            meterial = Meterial.objects.filter(pk=pk).first()
            if meterial:
                meterial.amount = data.get('amount', 0)
                meterial.save()
    return redirect(reverse_lazy('app-sklad-list'))

def delete_sklad(request, pk):
    meterial = Meterial.objects.get(pk=pk)
    meterial.delete()
    return redirect(reverse_lazy('app-sklad-list'))

class CategoryView(TemplateView):
    form_class = UserCategoryForm
    success_url = reverse_lazy('app-color-list')

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))        
        categories =  UserCategory.objects.order_by('name')
        context['form'] = self.form_class()
        context['items'] = categories
        context['type'] = 'category'

        return context
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect(self.success_url)
        else:
            print("Main Form Errors:", form.errors)
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)

class CategoryUpdateView(UpdateView):
    model = UserCategory
    form_class = UserCategoryForm
    success_url = reverse_lazy('app-category-list')
    
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['type'] = 'category'
        return context
    
def delete_category(request, pk):
    category = CategoryView.objects.get(pk=pk)
    category.delete()
    return redirect(reverse_lazy('app-category-list'))