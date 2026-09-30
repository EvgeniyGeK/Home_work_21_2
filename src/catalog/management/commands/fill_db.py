from django.core.management.base import BaseCommand
from django.db import connection
from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Наполнение базы данных начальными категориями и продуктами с очисткой таблиц"

    def handle(self, *args, **options):
        # 1. Очищаем таблицы перед заполнением
        self.stdout.write("Очистка таблиц базы данных...")
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Сбрасываем счетчики ID в PostgreSQL, чтобы нумерация начиналась с 1
        with connection.cursor() as cursor:
            cursor.execute("ALTER SEQUENCE catalog_category_id_seq RESTART WITH 1;")
            cursor.execute("ALTER SEQUENCE catalog_product_id_seq RESTART WITH 1;")

        # 2. Создаем начальные категории
        self.stdout.write("Создание категорий...")
        categories_data = [
            {"name": "Электроника", "description": "Смартфоны, ноутбуки и гаджеты"},
            {"name": "Инструменты", "description": "Ручной и электроинструмент для ремонта"},
            {"name": "Садоводство", "description": "Всё для ухода за садом и растениями"},
        ]

        categories_dict = {}
        for cat_item in categories_data:
            category = Category.objects.create(**cat_item)
            categories_dict[category.name] = category

        # 3. Создаем начальные продукты
        self.stdout.write("Создание продуктов...")
        products_data = [
            {
                "name": "Смартфон Samsung Galaxy S25",
                "description": "Флагманский смартфон с продвинутой камерой",
                "category": categories_dict["Электроника"],
                "price": 99990.00,
            },
            {
                "name": "Набор инструментов Makita",
                "description": "Профессиональный комплект для дома и мастерской",
                "category": categories_dict["Инструменты"],
                "price": 12500.00,
            },
            {
                "name": "Светодиодная фитолампа Uniel",
                "description": "Мощная лампа для выращивания комнатных растений и рассады",
                "category": categories_dict["Садоводство"],
                "price": 2450.00,
            },
        ]

        for prod_item in products_data:
            Product.objects.create(**prod_item)

        self.stdout.write(self.style.SUCCESS("База данных успешно наполнена начальными данными!"))

