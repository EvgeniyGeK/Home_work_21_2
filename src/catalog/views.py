from django.shortcuts import render, get_object_or_404
from catalog.models import Product, Contacts, Feedback


def home_view(request):
    """Контроллер для отображения домашней страницы"""
    latest_products = Product.objects.order_by("-created_at")[:5]

    print("\n--- ПОСЛЕДНИЕ 5 СОЗДАННЫХ ПРОДУКТОВ ---")
    for index, product in enumerate(latest_products, start=1):
        print(f"{index}. {product.name} | Дата создания: {product.created_at}")
    print("---------------------------------------\n")

    return render(request, "prototype_1.html")


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
