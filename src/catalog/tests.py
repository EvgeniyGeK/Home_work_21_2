from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product, Category
from django.utils.crypto import get_random_string

User = get_user_model()


class ProductAccessRightsTestCase(TestCase):

    def setUp(self):

        # Генерируем случайный пароль для текущей тестовой сессии
        self.test_password = get_random_string(length=16)

        # 1. Создаем пользователей с динамическим хэшированием пароля
        self.owner = User.objects.create(email='owner@test.com')
        self.owner.set_password(self.test_password)
        self.owner.save()

        self.stranger = User.objects.create(email='stranger@test.com')
        self.stranger.set_password(self.test_password)
        self.stranger.save()

        self.moderator = User.objects.create(email='moderator@test.com')
        self.moderator.set_password(self.test_password)
        self.moderator.save()

        # Назначаем модератору права
        moderator_group, _ = Group.objects.get_or_create(name='Модераторы')
        content_type = ContentType.objects.get_for_model(Product)
        perm_change = Permission.objects.get(codename='can_change_description', content_type=content_type)
        perm_unpublish = Permission.objects.get(codename='can_unpublish_product', content_type=content_type)

        # Добавляем права в ГРУППУ
        moderator_group.permissions.add(perm_change, perm_unpublish)

        # Добавляем модератора в эту ГРУППУ
        self.moderator.groups.add(moderator_group)
        self.moderator.save()

        # 2. Создаем тестовую категорию (обязательное поле для продукта!)
        self.category = Category.objects.create(
            name='Тестовая категория',
            description='Описание категории'
        )

        # 3. Создаем продукт, принадлежащий owner (передаем созданную категорию)
        self.product = Product.objects.create(
            name='Тестовый продукт',
            description='Описание',
            price=100,
            category=self.category,  # ДОБАВИЛИ ОБЯЗАТЕЛЬНОЕ ПОЛЕ
            owner=self.owner,
            is_published=True
        )



        # Ссылки на эндпоинты
        self.detail_url = reverse('catalog:product_detail', kwargs={'pk': self.product.pk})
        self.update_url = reverse('catalog:product_update', kwargs={'pk': self.product.pk})
        self.delete_url = reverse('catalog:product_delete', kwargs={'pk': self.product.pk})
        self.unpublish_url = reverse('catalog:product_unpublish', kwargs={'pk': self.product.pk})


    # --- ТЕСТЫ ДОСТУПА НА БЭКЕНДЕ (dispatch / POST) ---

    def test_owner_can_manage_product(self):
        """Владелец имеет право изменять и удалять свой продукт"""
        self.client.login(email='owner@test.com', password=self.test_password)

        # Редактирование (передаем категорию)
        response = self.client.post(self.update_url, {
            'name': 'Новое имя',
            'price': 150,
            'category': self.category.pk
        })
        self.assertIn(response.status_code, [200, 302])

        # Удаление
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)

    def test_stranger_cannot_manage_product(self):
        """Посторонний пользователь получает 403 Forbidden при попытке изменения/удаления"""
        self.client.login(email='stranger@test.com', password=self.test_password)

        # Проверяем блокировку изменения (ожидаем 403)
        response = self.client.post(self.update_url, {'name': 'Взлом', 'category': self.category.pk})
        self.assertEqual(response.status_code, 403)

        # Проверяем блокировку удаления (ожидаем 403)
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 403)

        # Проверяем блокировку снятия с публикации (ожидаем 403)
        response = self.client.post(self.unpublish_url)
        self.assertEqual(response.status_code, 403)

    # --- ТЕСТЫ ОТОБРАЖЕНИЯ КНОПОК В ШАБЛОНАХ ---

    def test_buttons_hidden_for_anonymous(self):
        """Анонимный пользователь вообще не имеет доступа к просмотру товара (Редирект 302)"""
        response = self.client.get(self.detail_url)
        # Так как наставник потребовал LoginRequiredMixin, ожидаем редирект 302 на авторизацию
        self.assertEqual(response.status_code, 302)

    def test_buttons_visibility_by_roles(self):
        """Проверка видимости кнопок в зависимости от роли вошедшего пользователя"""
        # 1. Владелец заходит на страницу товара
        self.client.login(email='owner@test.com', password=self.test_password)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.update_url)
        self.assertContains(response, self.delete_url)

        # 2. Посторонний заходит на страницу товара
        self.client.login(email='stranger@test.com', password=self.test_password)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.update_url)
        self.assertNotContains(response, self.delete_url)
