from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
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
        # Перехватываем объект, но еще не сохраняем в БД
        product = form.save(commit=False)
        # Автоматически назначаем владельцем текущего пользователя
        product.owner = self.request.user
        product.save()
        return super().form_valid(form)



class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """CBV для редактирования существующего товара с использованием ProductForm"""
    model = Product
    form_class = ProductForm
    template_name = "product_form.html"
    success_url = reverse_lazy("catalog:home")

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        # 2. Проверяем три условия допуска:
        # - Текущий пользователь — хозяин этого товара
        # - ИЛИ текущий пользователь — главный администратор (суперюзер)
        # - ИЛИ у пользователя есть кастомное право модератора
        if self.object.owner == request.user or request.user.is_superuser or request.user.has_perm(
                'catalog.can_change_description'):
            # Если хоть одно условие совпало — разрешаем открыть страницу формы
            return super().dispatch(request, *args, **kwargs)

        # 3. Если зашел чужой человек или бот — жестко блокируем и отдаем ошибку 403
        raise PermissionDenied


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """CBV для безопасного удаления товара из базы данных"""
    model = Product
    template_name = "blog/blogpost_confirm_delete.html"
    success_url = reverse_lazy("catalog:home")

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Удалять чужой товар модератор обычно не может, только автор (или суперпользователь)
        if self.object.owner == request.user or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied


class ContactsView(LoginRequiredMixin, View):
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

class CatalogTemplateView(LoginRequiredMixin, TemplateView):
    """CBV для страницы категорий"""
    template_name = "catalog.html"

class OrdersTemplateView(LoginRequiredMixin, TemplateView):
    """CBV для страницы заказов"""
    template_name = "orders.html"

