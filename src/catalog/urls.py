from django.urls import path
from catalog.views import home_view, contacts_view, catalog_view, orders_view


urlpatterns = [
    path('', home_view, name='home'),
    path('contacts/', contacts_view, name='contacts'),
    path('catalog/', catalog_view, name='catalog'),
    path('orders/', orders_view, name='orders'),
]

