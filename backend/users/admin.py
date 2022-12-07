from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'full_name', 'role', 'is_staff')
    fields = (
        ('username', 'email'), ('first_name', 'last_name'),
        'role', 'password', 'is_staff', 'is_active', 'date_joined'
    )
    add_fieldsets = (
        *UserAdmin.add_fieldsets,
        ('Регистрация',
            {'fields': (
                'first_name',
                'last_name',
                'email',
                'role'
            )}
         )
    )
    fieldsets = []
    search_fields = ('username',)
    list_filter = ('username', 'email')
    empty_value_display = '-пусто-'
    ordering = ('username',)

    def full_name(self, obj):
        full_name = '%s %s' % (obj.first_name, obj.last_name)
        return full_name.strip()
    full_name.short_description = 'Имя пользователя'
