from django.urls import path
from .views import (
    ProductsView, 
    ProductUpdateView, 
    delete_product, 
    ColorsView,
    ColorUpdateView,
    delete_color,
    SkladView,
    sklad_edit,
    delete_sklad,
    CategoryView,
    CategoryUpdateView,
    delete_category
    )
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path(
        "app/product/list/",
        login_required(ProductsView.as_view(template_name="app_product_list.html")),
        name="app-product-list",
    ),
    path(
        "app/product/create/",
        login_required(ProductsView.as_view(template_name="app_product_create.html")),
        name="app-product-create",
    ),
    path(
        "app/product/<int:pk>/edit/",
        login_required(ProductUpdateView.as_view(template_name="app_product_create.html")),
        name="app-product-edit",
    ),
    path(
        "app/product/<int:pk>/delete/",
        login_required(delete_product),
        name="app-product-delete",
    ),
    #Color
    
    path(
        "app/color/list/",
        login_required(ColorsView.as_view(template_name="app_product_list.html")),
        name="app-color-list",
    ),
    path(
        "app/color/create/",
        login_required(ColorsView.as_view(template_name="app_product_create.html")),
        name="app-color-create",
    ),
    path(
        "app/color/<int:pk>/edit/",
        login_required(ColorUpdateView.as_view(template_name="app_product_create.html")),
        name="app-color-edit",
    ),
    path(
        "app/color/<int:pk>/delete/",
        login_required(delete_color),
        name="app-color-delete",
    ),
    
    path(
        "app/category/list/",
        login_required(CategoryView.as_view(template_name="app_product_list.html")),
        name="app-category-list",
    ),
    path(
        "app/category/create/",
        login_required(CategoryView.as_view(template_name="app_product_create.html")),
        name="app-category-create",
    ),
    path(
        "app/category/<int:pk>/edit/",
        login_required(CategoryUpdateView.as_view(template_name="app_product_create.html")),
        name="app-category-edit",
    ),
    path(
        "app/category/<int:pk>/delete/",
        login_required(delete_category),
        name="app-category-delete",
    ),
    
    #Sklad
    path(
        "app/sklad/list/",
        login_required(SkladView.as_view(template_name="app_sklad_list.html")),
        name="app-sklad-list",
    ),
    path(
        "app/sklad/<int:pk>/edit/",
        login_required(sklad_edit),
        name="app-sklad-edit",
    ),
    path(
        "app/sklad/<int:pk>/delete/",
        login_required(delete_sklad),
        name="app-sklad-delete",
    ),
    
]
