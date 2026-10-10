from django.db import models

class BlogPost(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Заголовок",
        help_text="Введите заголовок статьи"
    )
    content = models.TextField(
        verbose_name="Содержимое",
        help_text="Введите текст статьи"
    )
    preview = models.ImageField(
        upload_to="blog/",
        blank=True,
        null=True,
        verbose_name="Превью (изображение)",
        help_text="Загрузите изображение для превью"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name="Признак публикации",
        help_text="Опубликовать ли статью на сайте сразу?"
    )
    views_count = models.IntegerField(
        default=0,
        verbose_name="Количество просмотров"
    )

    class Meta:
        verbose_name = "Блоговая запись"
        verbose_name_plural = "Блоговые записи"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
