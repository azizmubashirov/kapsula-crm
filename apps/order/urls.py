from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (
    RemainsView, 
    add_production_product,
    StockView,
    ProductHistoryView,
    edit_production_product,
    change_price_production_product,
    OrderView,
    OrderClientFolderView,
    order_payment,
    export_order_to_excel,
    DebtorsView,
    edit_shipment,
    order_edit,
    export_debtors_to_excel,
    add_payment,
    import_clients_from_excel,
    edit_folders,
    delete_order,
    export_product_history,
    export_to_excel_production_product,
    delete_folders,
    add_year,
    delete_quantity_production_product
)

urlpatterns = [
    path(
        "app/order-client/folders/",
        login_required(OrderClientFolderView.as_view(template_name="app_order_client_folder.html")),
        name="app-order-client-folder",
    ),
    path(
        "app/order-edit/folders/<int:pk>",
        login_required(edit_folders),
        name="app-order-edit-folder",
    ),
    path(
        "app/delete/folders/<int:pk>",
        login_required(delete_folders),
        name="app-delete-folder",
    ),
    path(
        "app/order/list/",
        login_required(OrderView.as_view(template_name="app_order_list.html")),
        name="app-order-list",
    ),
    path(
        "app/order/edit/<int:pk>",
        login_required(order_edit),
        name="app-edit-order",
    ),
    path(
        "app/order-payment/<int:pk>", order_payment, name="app-payment-order"
    ),
    path(
        "app/add-payment", add_payment, name="app-add-payment"
    ),
    path(
        "app/order/create/",
        login_required(OrderView.as_view(template_name="app_order_create.html")),
        name="app-order-create",
    ),
    path(
        "app/production-product/list/",
        login_required(RemainsView.as_view(template_name="app_remain_list.html")),
        name="app-production-product-list",
    ),
    path(
        "app/production-product/<int:pk>/create/",
        login_required(add_production_product),
        name="app-production-product-create",
    ),
    path(
        "app/production-product/<int:pk>/edit/",
        login_required(edit_production_product),
        name="app-production-product-edit",
    ),
    path(
        "app/production-product/<int:pk>/change-price/",
        login_required(change_price_production_product),
        name="app-production-product-change-price",
    ),
    path(
        "app/production-product/<int:pk>/delete-quantity/",
        login_required(delete_quantity_production_product),
        name="app-production-product-delete-quantity",
    ),
    path(
        "app/stock-history/list/",
        login_required(ProductHistoryView.as_view(template_name="app_product_history.html")),
        name="app-production-product-history-list",
    ),
    path(
        "app/production-history/list/",
        login_required(StockView.as_view(template_name="app_stock_history_list.html")),
        name="app-production-history-list",
    ),
    path(
        "app/debtors/",
        login_required(DebtorsView.as_view(template_name="app_debtors.html")),
        name="app-debtors",
    ),
    path(
        "app/edit-shipment",
        login_required(edit_shipment),
        name="app-shipment",
    ),
    path(
        "app/add-year/<int:pk>",
        login_required(add_year),
        name="app-add-year",
    ),
    path(
        "app/order/export/data", export_order_to_excel
    ),
    path(
        "app/debtors/export/data", export_debtors_to_excel
    ),
    path(
        "app/order-delete/<int:pk>", delete_order
    ),
    path(
        "app/import-order/clients", import_clients_from_excel
    ),
    path(
        "app/export-product-history", export_product_history
    ),
    path(
        "app/export-production-product", export_to_excel_production_product
    )
    
    
]
