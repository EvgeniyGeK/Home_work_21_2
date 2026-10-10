from django import forms
from catalog.models import Product, Category

FORBIDDEN_WORDS = [
    "казино", "криптовалюта", "крипта", "биржа",
    "дешево", "бесплатно", "обман", "полиция", "радар"
]


class ProductForm(forms.ModelForm):
    category = forms.CharField(
        max_length=150,
        label="Категория товара",
        help_text="Например: Электроника, Инструменты, Садоводство, Лабораторное оборудование",
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите название категории вручную...',
            'class': 'form-control'
        })
    )
    image = forms.ImageField(
        label="Изображение товара",
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        error_messages={
            'invalid_image': 'Ошибка: Неподдерживаемый формат файла или файл повреждён! Разрешено загружать только изображения (JPEG/PNG).',
            'missing': 'Файл изображения отсутствует.',
            'empty': 'Загруженный файл пуст.'
        }
    )

    class Meta:
        model = Product
        fields = ("name", "description", "image", "category", "price")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.category:
            self.initial['category'] = self.instance.category.name

        for field_name, field in self.fields.items():
            if field_name != 'category':  # Категорию мы уже настроили выше
                if isinstance(field.widget, forms.CheckboxInput):
                    field.widget.attrs['class'] = 'form-check-input'
                else:
                    field.widget.attrs['class'] = 'form-control'

    def clean_category(self):
        """
        Валидация ручного текстового ввода категории.
        Ищет совпадение по имени в базе данных без учета регистра.
        """
        category_name = self.cleaned_data.get("category").strip()

        if not category_name:
            raise forms.ValidationError("Поле категории является обязательным для заполнения.")

        category_obj = Category.objects.filter(name__iexact=category_name).first()

        if not category_obj:
            raise forms.ValidationError(
                f"Категория '{category_name}' не найдена в базе данных. "
                f"Пожалуйста, введите существующую категорию или создайте её в админ-панели."
            )

        return category_obj

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is not None and price < 0:
            raise forms.ValidationError(
                "Ошибка: Цена за покупку не может быть отрицательной! Укажите корректное положительное число."
            )
        return price

    def clean_name(self):
        name = self.cleaned_data.get("name")
        name_lower = name.lower()
        for word in FORBIDDEN_WORDS:
            if word in name_lower:
                raise forms.ValidationError(f"Название продукта содержит запрещенное спам-слово '{word}'.")
        return name

    def clean_description(self):
        description = self.cleaned_data.get("description")
        if description:
            description_lower = description.lower()
            for word in FORBIDDEN_WORDS:
                if word in description_lower:
                    raise forms.ValidationError(f"Описание продукта содержит запрещенное спам-слово '{word}'.")
        return description

    def clean_image(self):
        """Валидация формата (JPEG/PNG) и размера (до 5 МБ) изображения продукта"""
        image = self.cleaned_data.get("image")

        if not image:
            return image

        max_size = 5 * 1024 * 1024  # 5 МБ
        if image.size > max_size:
            raise forms.ValidationError(
                "Ошибка: Размер изображения превышает допустимый лимит 5 МБ. "
                "Пожалуйста, сожмите картинку или выберите другой файл."
            )

        file_name = image.name.lower()
        valid_extensions = ['.jpg', '.jpeg', '.png']

        has_valid_extension = any(file_name.endswith(ext) for ext in valid_extensions)

        valid_content_types = ['image/jpeg', 'image/png', 'image/pjpeg', 'image/x-png']

        if not has_valid_extension or image.content_type not in valid_content_types:
            raise forms.ValidationError(
                "Ошибка: Неподдерживаемый формат файла! "
                "Разрешено загружать изображения только в форматах JPEG (JPG) или PNG."
            )

        return image