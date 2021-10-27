import graphene
from graphene_django import DjangoObjectType

from ingredients.models import Category, Ingredient

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name", "ingredients")

class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "notes", "category")

class Query(graphene.ObjectType):
    all_ingredients = graphene.List(IngredientType)
    category_by_name = graphene.Field(CategoryType, name=graphene.String(required=True))
    all_categories = graphene.List(CategoryType)

    def resolve_all_ingredients(root, info):
        # We can easily optimize query count in the resolve method
        return Ingredient.objects.select_related("category").all()

    def resolve_category_by_name(root, info, name):
        try:
            return Category.objects.get(name=name)
        except Category.DoesNotExist:
            return None
    
    def resolve_all_categories(root, info):
        # We can easily optimize query count in the resolve method
        return Category.objects.all()

# schema = graphene.Schema(query=Query)


# class CreateCategory(graphene.Mutation):

#     class Arguments:
#         name = graphene.String()

#     def mutate(self, info, name):
#         category = Category(name=name)
#         category.save()

#         return CreateCategory(
#             id=category.id,
#             name=category.name,
#         )


# class UpdateCategory(graphene.Mutation):

#     class Arguments:
#         id = graphene.ID()
#         name = graphene.String()
    
#     category = graphene.Field(CategoryType)

#     @classmethod
#     def mutate(cls, root, info, id, name):
#         category = Category.objects.get(pk=id)
#         category.name = name
#         category.save()

#         return UpdateCategory(
#             category=category
#         )


class DeleteCategory(graphene.Mutation):

    class Arguments:
        id = graphene.ID()
    
    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, id):
        category = Category.objects.get(pk=id)
        category.delete()


# class Mutation(graphene.ObjectType):
#     create_category = CreateCategory.Field()


# class Mutation(graphene.ObjectType):
#     update_category = UpdateCategory.Field()


class Mutation(graphene.ObjectType):
    delete_category = DeleteCategory.Field()