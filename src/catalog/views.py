from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, TemplateView

from catalog.models import Product, Contacts, Feedback


class ProductListView(ListView):
    """CBV для отображения главной страницы со списком товаров и пагинацией"""
    model = Product
    template_name = "prototype_1.html"
    context_object_name = "page_obj"
    paginate_by = 3
    queryset = Product.objects.all()


class ProductDetailView(DetailView):
    """CBV для детальной страницы конкретного товара по его ID (pk)"""
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"


class ProductCreateView(CreateView):
    """CBV для создания нового товара через форму на сайте"""
    model = Product
    template_name = "product_form.html"

    fields = ("name", "description", "image", "category", "price")

    success_url = reverse_lazy("catalog:home")


class ContactsView(View):
    """CBV для страницы контактов с выводом данных и ручной валидацией POST-формы"""

    def get(self, request, *args, **kwargs):
        """Обработка GET-запроса: вывод страницы и данных из БД"""
        contact_info = Contacts.objects.first()
        return render(request, "contacts.html", {"contact_info": contact_info})

    def post(self, request, *args, **kwargs):
        """Обработка POST-запроса: валидация, сохранение обращения и вывод алерта"""
        contact_info = Contacts.objects.first()
        name = request.POST.get("username")
        email = request.POST.get("email")
        message = request.POST.get("message")

        context = {"contact_info": contact_info}


        if name and email and message:
            Feedback.objects.create(name=name, email=email, message=message)
            context["success"] = True
        else:
            context["error"] = "Пожалуйста, заполните все обязательные поля формы."

        return render(request, "contacts.html", context)

class CatalogTemplateView(TemplateView):
    """CBV для страницы категорий"""
    template_name = "catalog.html"

class OrdersTemplateView(TemplateView):
    """CBV для страницы заказов"""
    template_name = "orders.html"

