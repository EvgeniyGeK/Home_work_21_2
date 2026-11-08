from django.core.cache import cache
from config import settings
from catalog.models import Product


def get_products_by_category(category_id):
    """Сервисная функция для получения списка продуктов в категории с кешированием"""
    if not settings.CACHE_ENABLED:
        return Product.objects.filter(category_id=category_id, is_published=True)
    # Формируем уникальный ключ для кеша Redis
    key = f'products_category_{category_id}'
    # Пытаемся достать список из кеша
    products = cache.get(key)
    # Если в кеше пусто — берем из базы данных и записываем в Redis на 15 минут
    if products is None:
        products = list(Product.objects.filter(category_id=category_id, is_published=True))
        cache.set(key, products, timeout=900)

    return products
