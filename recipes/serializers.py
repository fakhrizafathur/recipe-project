from rest_framework import serializers
from .models import Recipe, Category, Ingredient

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'quantity']


class RecipeSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), write_only=True
    )  # Hanya untuk pengiriman ID kategori
    category_detail = CategorySerializer(source='category', read_only=True)  # Untuk membaca detail kategori
    ingredients = IngredientSerializer(many=True)  # Nested serialization untuk ingredients
    created_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S%z", read_only=True)

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'description', 'category', 'category_detail', 'ingredients', 'created_at']

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)

        for ingredient_data in ingredients_data:
            Ingredient.objects.create(recipe=recipe, **ingredient_data)

        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients', [])
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)

        # Update kategori
        if 'category' in validated_data:
            instance.category = validated_data['category']

        instance.save()

        # Update ingredients
        for ingredient_data in ingredients_data:
            ingredient_id = ingredient_data.get('id', None)
            if ingredient_id:
                ingredient = Ingredient.objects.get(id=ingredient_id)
                ingredient.name = ingredient_data.get('name', ingredient.name)
                ingredient.quantity = ingredient_data.get('quantity', ingredient.quantity)
                ingredient.save()
            else:
                Ingredient.objects.create(recipe=instance, **ingredient_data)

        return instance


# from rest_framework import serializers
# from .models import Recipe, Category, Ingredient

# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ['id', 'name']

# class IngredientSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Ingredient
#         fields = ['id', 'name', 'quantity']

# class RecipeSerializer(serializers.ModelSerializer):
#     category = serializers.PrimaryKeyRelatedField(
#         queryset=Category.objects.all(), write_only=True
#     )  # Hanya untuk pengiriman ID kategori
#     category_detail = CategorySerializer(source='category', read_only=True)  # Untuk membaca detail kategori
#     ingredients = IngredientSerializer(many=True)  # Nested serialization untuk ingredients
#     created_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S%z", read_only=True)

#     class Meta:
#         model = Recipe
#         fields = ['id', 'name', 'description', 'category', 'category_detail', 'ingredients', 'created_at']

#     def create(self, validated_data):
#         ingredients_data = validated_data.pop('ingredients')
#         recipe = Recipe.objects.create(**validated_data)

#         for ingredient_data in ingredients_data:
#             Ingredient.objects.create(recipe=recipe, **ingredient_data)

#         return recipe

#     def update(self, instance, validated_data):
#         ingredients_data = validated_data.pop('ingredients', [])
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)

#         # Update kategori
#         if 'category' in validated_data:
#             instance.category = validated_data['category']

#         instance.save()

#         # Update ingredients
#         for ingredient_data in ingredients_data:
#             ingredient_id = ingredient_data.get('id', None)
#             if ingredient_id:
#                 ingredient = Ingredient.objects.get(id=ingredient_id)
#                 ingredient.name = ingredient_data.get('name', ingredient.name)
#                 ingredient.quantity = ingredient_data.get('quantity', ingredient.quantity)
#                 ingredient.save()
#             else:
#                 Ingredient.objects.create(recipe=instance, **ingredient_data)

#         return instance


