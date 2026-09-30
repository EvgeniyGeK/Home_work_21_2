from django.shortcuts import render
from catalog.models import Product, Contacts


def home_view(request):
    """Контроллер для отображения домашней страницы"""
    latest_products = Product.objects.order_by("-created_at")[:5]

    print("\n--- ПОСЛЕДНИЕ 5 СОЗДАННЫХ ПРОДУКТОВ ---")
    for index, product in enumerate(latest_products, start=1):
        print(f"{index}. {product.name} | Дата создания: {product.created_at}")
    print("---------------------------------------\n")

    return render(request, "prototype_1.html")


def contacts_view(request):
    """Контроллер для контактов с обработкой формы обратной связи"""
    contact_info = Contacts.objects.first()

    context = {
        "contact_info": contact_info,
    }

    if request.method == "POST":
        name = request.POST.get("username")
        email = request.POST.get("email")
        message = request.POST.get("message")

        print(f"\n[Обратная связь]: Имя: {name}, Email: {email}, Сообщение: {message}\n")
        context["success"] = True

    return render(request, "contacts.html", context)


    if request.method == 'POST':
        name = request.POST.get('username')
        email = request.POST.get('email')
        message = request.POST.get('message')


        print(f"\n[Обратная связь]: Имя: {name}, Email: {email}, Сообщение: {message}\n")


        context['success'] = True

    return render(request, 'contacts.html', context)


def catalog_view(request):
    """Контроллер для страницы каталога (категорий)"""
    return render(request, 'catalog.html')


def orders_view(request):
    """Контроллер для страницы заказов"""
    return render(request, 'orders.html')

