from django.contrib import admin
from catalog.models import Category, Product
from catalog.models import Contacts
from catalog.models import Feedback


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "category")
    list_filter = ("category",)
    search_fields = ("name", "description")

    @admin.register(Contacts)
    class ContactsAdmin(admin.ModelAdmin):
        list_display = ("id", "phone", "email", "address")



@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "created_at")
    search_fields = ("name", "email", "message")
