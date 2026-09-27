from django.shortcuts import render


def home_view(request):
    """Контроллер для отображения домашней страницы"""
    return render(request, 'prototype_1.html')


def contacts_view(request):
    """Контроллер для отображения контактов и обработки POST-данных"""
    context = {}
    if request.method == 'POST':
        name = request.POST.get('username')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Печатаем принятые данные в консоль PyCharm
        print(f"\n[Обратная связь]: Имя: {name}, Email: {email}, Сообщение: {message}\n")
        context['success'] = True

    return render(request, 'contacts.html', context)

