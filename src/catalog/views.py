from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from catalog.models import Product, Contacts, Feedback, Category


def home_view(request):
    """Контроллер главной страницы с поддержкой постраничного вывода (пагинации)"""
    products_list = Product.objects.all()
    paginator = Paginator(products_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    latest_products = Product.objects.order_by("-created_at")[:5]
    print("\n--- ПОСЛЕДНИЕ 5 СОЗДАННЫХ ПРОДУКТОВ ---")
    for index, product in enumerate(latest_products, start=1):
        print(f"{index}. {product.name}")
    print("---------------------------------------\n")

    return render(request, 'prototype_1.html', {'page_obj': page_obj})


def contacts_view(request):
    contact_info = Contacts.objects.first()
    context = {"contact_info": contact_info}

    if request.method == "POST":
        name = request.POST.get("username")
        email = request.POST.get("email")
        message = request.POST.get("message")

        # Защита от ошибок и валидация: проверяем, что все поля заполнены (Выполнение критерия)
        if name and email and message:
            # Сохраняем обращение напрямую в базу данных PostgreSQL
            Feedback.objects.create(name=name, email=email, message=message)
            context["success"] = True
        else:
            context["error"] = "Пожалуйста, заполните все поля формы."

    return render(request, "contacts.html", context)


def catalog_view(request):
    """Контроллер для страницы каталога (категорий)"""
    return render(request, 'catalog.html')


def orders_view(request):
    """Контроллер для страницы заказов"""
    return render(request, 'orders.html')


def product_detail_view(request, pk):
    """
    Контроллер для отображения детальной информации о товаре.
    Получает pk из URL, извлекает объект через ORM и передает его в шаблон.
    """
    product = get_object_or_404(Product, pk=pk)
    context = {
        'product': product
    }
    return render(request, 'product_detail.html', context)


def product_create_view(request):
    """Контроллер для страницы создания нового товара с валидацией и сохранением в БД"""
    categories = Category.objects.all()
    context = {
        'categories': categories
    }

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        image = request.FILES.get('image')

        if name and price and category_id:
            try:
                category = Category.objects.get(pk=category_id)

                new_product = Product.objects.create(
                    name=name,
                    description=description,
                    price=price,
                    category=category,
                    image=image
                )
                return redirect('catalog:home')
            except (Category.DoesNotExist, ValueError):
                context['error'] = "Переданы некорректные данные. Проверьте цену и категорию."
        else:
            context['error'] = "Пожалуйста, заполните все обязательные поля (Наименование, Цена, Категория)."

    return render(request, 'product_form.html', context)

