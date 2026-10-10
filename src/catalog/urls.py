from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import (
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ContactsView,
    CatalogTemplateView,
    OrdersTemplateView,
)

app_name = CatalogConfig.name

urlpatterns = [

    path("", ProductListView.as_view(), name="home"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path("catalog/", CatalogTemplateView.as_view(), name="catalog"),
    path("orders/", OrdersTemplateView.as_view(), name="orders"),
]


