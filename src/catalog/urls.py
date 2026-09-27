from django.urls import path
from catalog.views import home_view, contacts_view


urlpatterns = [
    path('', home_view, name='home'),
    path('contacts/', contacts_view, name='contacts'),
]

