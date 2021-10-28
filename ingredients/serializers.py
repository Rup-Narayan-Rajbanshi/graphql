from rest_framework import serializers
from .models import Ingredient, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
        )


# class IngredientsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Ingredients
#         fields = (
#             'id',
#             'name',
#             'notes',
#             'category',
#         )