from django import forms
from catalog.models import Product


FORBIDDEN_WORDS = [
    "казино", "криптовалюта", "крипта", "биржа",
    "дешево", "бесплатно", "обман", "полиция", "радар"
]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("name", "description", "image", "category", "price")

    def clean_name(self):
        """Валидация поля 'name' на отсутствие спам-слов с игнорированием регистра"""
        name = self.cleaned_data.get("name")

        name_lower = name.lower()

        for word in FORBIDDEN_WORDS:
            if word in name_lower:
                raise forms.ValidationError(
                    f"Название продукта содержит запрещенное спам-слово '{word}'. Пожалуйста, измените название."
                )
        return name

    def clean_description(self):
        """Валидация поля 'description' на отсутствие спам-слов с игнорированием регистра"""
        description = self.cleaned_data.get("description")

        if description:
            description_lower = description.lower()

            for word in FORBIDDEN_WORDS:
                if word in description_lower:
                    raise forms.ValidationError(
                        f"Описание продукта содержит запрещенное спам-слово '{word}'. Пожалуйста, измените текст."
                    )
        return description
