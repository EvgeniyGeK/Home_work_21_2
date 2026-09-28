from django.shortcuts import render


def home_view(request):
    """Контроллер для отображения домашней страницы"""
    return render(request, 'prototype_1.html')


def contacts_view(request):
    """Контроллер для контактов с обработкой формы обратной связи"""
    context = {}


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

