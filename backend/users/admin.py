from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('id', 'username', 'first_name', 'last_name', 'role')
    fields = (
        ('username', 'email'), ('first_name', 'last_name'), 'role'
    )
    add_fieldsets = (
        *UserAdmin.add_fieldsets,
        (
            'Custom fields',
            {
                'fields': (
                    'first_name',
                    'last_name',
                    'email'
                )
            }
        )
    )
    fieldsets = []
    search_fields = ('username',)
    list_filter = ('username', 'email')
    empty_value_display = '-пусто-'
