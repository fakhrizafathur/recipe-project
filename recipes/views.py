from rest_framework import viewsets
from .models import Recipe, Category
from .serializers import RecipeSerializer, CategorySerializer

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def list(self, request, *args, **kwargs):
        category_id = request.query_params.get('category', None)
        if category_id:
            self.queryset = self.queryset.filter(category_id=category_id)
        return super().list(request, *args, **kwargs)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# from rest_framework import viewsets
# from rest_framework.response import Response
# from rest_framework.decorators import action
# from .models import Recipe, Category,Ingredient
# from .serializers import RecipeSerializer, CategorySerializer

# class RecipeViewSet(viewsets.ModelViewSet):
#     queryset = Recipe.objects.all()
#     serializer_class = RecipeSerializer

#     # Override list method to allow filtering by category
#     def list(self, request, *args, **kwargs):
#         category_id = request.query_params.get('category', None)
#         if category_id:
#             self.queryset = self.queryset.filter(category_id=category_id)
#         return super().list(request, *args, **kwargs)
    
#     # Update method to handle updating recipe, category, and ingredients
#     def update(self, request, *args, **kwargs):
#         recipe = self.get_object()
#         data = request.data
        
#         # Update recipe details
#         recipe.name = data.get('name', recipe.name)
#         recipe.description = data.get('description', recipe.description)
        
#         # Update category
#         category_id = data.get('category', None)
#         if category_id:
#             category = Category.objects.get(id=category_id)
#             recipe.category = category
        
#         # Update ingredients
#         ingredients_data = data.get('ingredients', [])
#         for ingredient_data in ingredients_data:
#             ingredient_id = ingredient_data.get('id', None)
#             if ingredient_id:
#                 ingredient = Ingredient.objects.get(id=ingredient_id)
#                 ingredient.name = ingredient_data.get('name', ingredient.name)
#                 ingredient.quantity = ingredient_data.get('quantity', ingredient.quantity)
#                 ingredient.save()
#             else:
#                 Ingredient.objects.create(
#                     recipe=recipe,
#                     name=ingredient_data.get('name'),
#                     quantity=ingredient_data.get('quantity')
#                 )
        
#         recipe.save()
#         return Response(RecipeSerializer(recipe).data)

# class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
