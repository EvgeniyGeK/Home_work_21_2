from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from catalog.models import Product, Contacts, Feedback
from catalog.forms import ProductForm



class ProductListView(ListView):
    """CBV для отображения главной страницы со списком товаров и пагинацией"""
    model = Product
    template_name = "prototype_1.html"
    context_object_name = "page_obj"
    paginate_by = 3



class ProductDetailView(LoginRequiredMixin, DetailView):
    """CBV для детальной страницы конкретного товара по его ID (pk)"""
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"


class ProductCreateView(LoginRequiredMixin, CreateView):
    """CBV для создания нового товара через форму на сайте"""
    model = Product
    form_class = ProductForm
    template_name = "product_form.html"
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        # 1. Привязываем текущего пользователя к полю owner формы, не сохраняя в БД
        form.instance.owner = self.request.user
        return super().form_valid(form)

def can_manage_product(user, product):
    is_owner = product.owner_id == user.id
    is_moderator = (
        user.has_perm("catalog.can_change_description")
        or user.has_perm("catalog.can_unpublish_product")
    )
    return is_owner or is_moderator or user.is_superuser


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """CBV для редактирования существующего товара с использованием ProductForm"""
    model = Product
    form_class = ProductForm
    template_name = "product_form.html"
    success_url = reverse_lazy("catalog:home")



    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        if not can_manage_product(request.user, product):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """CBV для безопасного удаления товара из базы данных"""
    model = Product
    template_name = "blog/blogpost_confirm_delete.html"
    success_url = reverse_lazy("catalog:home")

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        if not can_manage_product(request.user, product):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class ContactsView(LoginRequiredMixin, View):
    """CBV для страницы контактов с выводом данных и ручной валидацией POST-формы"""

    def get(self, request, *args, **kwargs):
        """Обработка GET-запроса: вывод страницы и данных из БД"""
        contact_info = Contacts.objects.first()
        return render(request, "contacts.html", {"contact_info": contact_info})

    def post(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)

        # Используем единую функцию проверки прав
        if can_manage_product(request.user, product):
            product.is_published = False
            product.save()
            return redirect("catalog:product_detail", pk=pk)

        raise PermissionDenied

class CatalogTemplateView(LoginRequiredMixin, TemplateView):
    """CBV для страницы категорий"""
    template_name = "catalog.html"

class OrdersTemplateView(LoginRequiredMixin, TemplateView):
    """CBV для страницы заказов"""
    template_name = "orders.html"


class ProductUnpublishView(LoginRequiredMixin, View):
    """Контроллер для снятия продукта с публикации модератором"""

    def post(self, request, pk, *args, **kwargs):
        # 1. Извлекаем продукт по его id
        product = get_object_or_404(Product, pk=pk)

        # 2. Проверяем наличие конкретного права модератора
        if request.user.has_perm("can_unpublish_product"):
            product.is_published = False
            product.save()
            return redirect("catalog:product_detail", pk=pk)  # Возвращаем на страницу товара

        # 3. Если права нет — выкидываем ошибку доступа
        raise PermissionDenied
