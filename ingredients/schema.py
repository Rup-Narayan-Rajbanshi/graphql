import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
import django_filters
from graphene_django.rest_framework.mutation import SerializerMutation

from ingredients.models import Category, Ingredient
from .serializers import CategorySerializer

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name", "ingredients")
        filter_fields = ["name", "ingredients"]
        interfaces = (relay.Node, )

class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "notes", "category")
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'notes': ['exact', 'icontains'],
            'category': ['exact'],
            'category__name': ['exact'],
        }
        interfaces = (relay.Node, )


class IngredientsFilter(django_filters.FilterSet):
    # Do case-insensitive lookups on 'name'
    # name = django_filters.CharFilter(field_name='name', lookup_expr=['iexact'])
    name = django_filters.CharFilter(field_name='name', lookup_expr='iexact')

    class Meta:
        model = Ingredient
        fields = ['name']
    
    # @property
    # def qs(self):
    #     # The query context can be found in self.request.
    #     return super(IngredientsFilter, self).qs.filter(category__name__iexact='Meat Product')


class Query(graphene.ObjectType):
    # all_ingredients = graphene.List(IngredientType)
    # category_by_name = graphene.Field(CategoryType, name=graphene.String(required=True))
    # all_categories = graphene.List(CategoryType)

    ingredients = relay.Node.Field(IngredientType)
    all_ingredients = DjangoFilterConnectionField(IngredientType, filterset_class=IngredientsFilter)

    category = relay.Node.Field(CategoryType)
    all_categories = DjangoFilterConnectionField(CategoryType)

    # def resolve_all_ingredients(root, info):
    #     # We can easily optimize query count in the resolve method
    #     return Ingredient.objects.select_related("category").all()

    # def resolve_category_by_name(root, info, name):
    #     try:
    #         return Category.objects.get(name=name)
    #     except Category.DoesNotExist:
    #         return None
    
    # def resolve_all_categories(root, info):
    #     # We can easily optimize query count in the resolve method
    #     return Category.objects.all()

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

class DeleteCategory(graphene.Mutation):
    ok = graphene.Boolean()
    
    class Arguments:
        id = graphene.ID()
    
    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, id):
        category = Category.objects.get(pk=id)
        category.delete()
        return cls(ok=True)


# mutation using serializer
class CreateCategory(SerializerMutation):
    delete_category = DeleteCategory.Field()

    class Meta:
        serializer_class = CategorySerializer
        model_operations = ['create', 'update']
        lookup_field = 'id'


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




class Mutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
    # delete_category = DeleteCategory.Field()

# class Mutation(graphene.ObjectType):
#     update_category = UpdateCategory.Field()


# class Mutation(graphene.ObjectType):
#     delete_category = DeleteCategory.Field()