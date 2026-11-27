from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create the product moderators group and assign permissions"

    def handle(self, *args, **options):
        group, _ = Group.objects.get_or_create(name="Модератор продуктов")
        permissions = Permission.objects.filter(
            content_type__app_label="catalog",
            codename__in=(
                "can_unpublish_product",
                "can_change_description",
            ),
        )
        group.permissions.set(permissions)
        self.stdout.write(self.style.SUCCESS("Moderator group is ready"))

