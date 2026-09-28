from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name="Наименование",
        help_text="Введите наименование категории"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание",
        help_text="Введите описание категории"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name="Наименование",
        help_text="Введите наименование продукта"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание",
        help_text="Введите описание продукта"
    )
    image = models.ImageField(
        upload_path="products/",
        blank=True,
        null=True,
        verbose_name="Изображение",
        help_text="Загрузите изображение продукта"
    )
    # Связь с моделью Category (Один ко многим)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категория",
        help_text="Выберите категорию продукта"
    )
    price = models.DecimalField(
        max_length=10,
        decimal_places=2,
        verbose_name="Цена за покупку",
        help_text="Укажите цену продукта"
    )

    # Общепринятые стандарты дат
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата последнего изменения"
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} (Цена: {self.price})"
