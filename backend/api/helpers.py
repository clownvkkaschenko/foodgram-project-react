from django.shortcuts import get_object_or_404
from recipes.models import QuantityOfIngredients
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST)


class Helper:
    """Класс созданный для вспомогательных методов."""
    def create_or_update_ingredients(self, instance, validated_data):
        """Добавление ингредиентов в рецепт, при его создании/обновлении."""
        for ingredient in validated_data:
            QuantityOfIngredients.objects.create(
                recipe=instance,
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount')
            )

    def post_or_delete(self, pk, instance):
        """Добавление/удаление объекта из выбранного поля(instance)"""
        pattern = get_object_or_404(self.queryset, id=pk)
        validate_pattern = instance.filter(id=pk).exists()
        serializer = self.additional_serializer(
            pattern, context={'request': self.request}
        )

        if self.request.method == 'POST' and not validate_pattern:
            instance.add(pattern)
            return Response(serializer.data, status=HTTP_201_CREATED)
        if self.request.method == 'DELETE' and validate_pattern:
            instance.remove(pattern)
            return Response(status=HTTP_204_NO_CONTENT)
        return Response(status=HTTP_400_BAD_REQUEST)
