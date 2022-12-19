from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'full_name_user', 'role', 'is_staff', 'sub')
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
    list_filter = []
    search_fields = ('username', 'email')
    ordering = ('username',)
    empty_value_display = '-пусто-'

    def full_name_user(self, obj):
        full_name = '%s %s' % (obj.first_name, obj.last_name)
        return full_name.strip()
    full_name_user.short_description = 'Имя пользователя'

    def sub(self, obj):
        return obj.subscriber.count()
    sub.short_description = 'В подписках'
