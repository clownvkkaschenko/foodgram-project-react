from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrReadonlyPermission(BasePermission):
    """Кастомное разрешение для изменения рецепта.

    Уровени доступа:
        - аноним: может просматривать материалы.
        - авторизованный пользователь: может постить.
        - автор: может редактировать и удалять свои материалы.
    """
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and obj.author == request.user
        )
