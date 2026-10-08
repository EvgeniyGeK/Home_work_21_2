from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from blog.models import BlogPost

class BlogPostListView(ListView):
    """CBV для вывода списка всех опубликованных статей"""
    model = BlogPost
    template_name = "blog/blogpost_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        """Выводим только те статьи, у которых стоит признак публикации"""
        return BlogPost.objects.filter(is_published=True)

class BlogPostDetailView(DetailView):
    """CBV для детального просмотра статьи с динамическим подсчетом просмотров и уведомлением на почту"""
    model = BlogPost
    template_name = "blog/blogpost_detail.html"
    context_object_name = "post"

    def get_object(self, queryset=None):
        """Переопределяем метод для увеличения счетчика и отправки email при 100 просмотрах"""
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save()


        if obj.views_count == 100:
            send_mail(
                subject="Поздравляем! Статья достигла 100 просмотров! 🎉",
                message=(
                    f"Ваша статья '{obj.title}' пользуется большой популярностью "
                    f"и только что набрала 100 просмотров на сайте.\n"
                    f"Продолжайте в том же духе!"
                ),
                from_email=None,
                recipient_list=["your-email@example.com"],
                fail_silently=True,
            )

        return obj


class BlogPostCreateView(CreateView):
    """CBV для создания новой блоговой записи через веб-форму"""
    model = BlogPost
    template_name = "blog/blogpost_form.html"
    fields = ("title", "content", "preview", "is_published")
    success_url = reverse_lazy("blog:list")

class BlogPostUpdateView(UpdateView):
    """CBV для редактирования существующей блоговой записи"""
    model = BlogPost
    template_name = "blog/blogpost_form.html"
    fields = ("title", "content", "preview", "is_published")

    def get_success_url(self):
        """После редактирования возвращаем пользователя на детальную страницу статьи"""
        return reverse("blog:detail", kwargs={"pk": self.object.pk})

class BlogPostDeleteView(DeleteView):
    """CBV для удаления статьи с подтверждением"""
    model = BlogPost
    template_name = "blog/blogpost_confirm_delete.html"
    success_url = reverse_lazy("blog:list")

