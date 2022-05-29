"""
Serializers for recipe APIs
"""

from core.models import Ingredient, Recipe, Tag
from rest_framework import serializers


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredients."""

    class Meta:
        model = Ingredient
        fields = ['id', 'name']
        read_only_fields = ['id']


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes."""
    # Now, we'll get to work with our TagSerializer in this serializer
    # it's kind of similar to a ForeignKey relationship in models.
    tags = TagSerializer(many=True, required=False)
    ingredients = IngredientSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        # Add 'tags' & 'ingredients' to fields
        fields = [
            'id', 'title', 'time_minutes', 'price', 'link', 'tags',
            'ingredients'
        ]
        read_only_fields = ['id']

    # NAMED THIS METHOD WITH UNDERSCORE, CAUSE WE INTENT TO USE IT INTERNALLY ONLY!
    # I.E. IT'S USED BY ONLY THIS SPECIFIC "RecipeSerializer" SERIALIZER.
    def _get_or_create_tags(self, tags, recipe):
        """
        Handle getting or creating tags as needed.
        i.e -> Get a tag or create one
        """
        # Next, let's get our (authenticated) user requesting the serializer
        auth_user = self.context['request'].user

        # Next, we'll create a for loop
        for tag in tags:
            # Let's call 'get_or_create', which get's or creates a value
            # depending whether it's already in our database
            # THE FUNCTIONALITY TO NOT CREATE DUPLICATE TAGS IN OUR SYSTEM!
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                # Instead of writing name=tag['name'], we write it this way, because,
                # if in the future we want the tags to have some other fields than
                # just name, this functionality supports that.
                **tag,
            )
            recipe.tags.add(tag_obj)

    # NAMED THIS METHOD WITH UNDERSCORE, CAUSE WE INTENT TO USE IT INTERNALLY ONLY!
    # I.E. IT'S USED BY ONLY THIS SPECIFIC "RecipeSerializer" SERIALIZER.
    def _get_or_create_ingredients(self, ingredients, recipe):
        """
        Handle getting or creating ingredients as needed.
        i.e -> Get an ingredient or create one
        """
        auth_user = self.context['request'].user
        for ingredient in ingredients:
            ingredient_obj, create = Ingredient.objects.get_or_create(
                user=auth_user,
                **ingredient,
            )
            recipe.ingredients.add(ingredient_obj)

    def create(self, validated_data):
        """Create a recipe."""
        # First, let's assign all tags from data, and assign it to a
        # variable (that's a list) called tags.
        tags = validated_data.pop('tags', [])
        ingredients = validated_data.pop('ingredients', [])
        # Then, with rest of the data (excluding tags), we'll create a new
        # recipe with those values
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_tags(tags, recipe)
        self._get_or_create_ingredients(ingredients, recipe)

        return recipe

    # Because we're updating an instance, we need to have 'instance' as a parameter
    def update(self, instance, validated_data):
        """Update recipe."""
        # Let's store the tags in 'tags' variable &
        # if there are no tags set it to 'None'
        tags = validated_data.pop('tags', None)
        ingredients = validated_data.pop('ingredients', None)
        # If the 'tags' variable contains tags, we'll clear them and call our
        # '_get_or_create_tags' function
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)
        if ingredients is not None:
            instance.ingredients.clear()
            self._get_or_create_ingredients(ingredients, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class RecipeDetailSerializer(RecipeSerializer):
    """
    Serializer for recipe detail view.

    We're using 'RecipeSerializer' as the parameter here because the detail
    serializer is going to be an extension of the 'RecipeSerializer'
    So, we want to take the functionality of that serializer &
    add some extra fields into our detail serializer.
    NOW, WE CAN AVOID DUPLICATE CODE!
    """

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description', 'image']


class RecipeImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to recipes."""

    class Meta:
        model = Recipe
        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {'image': {'required': 'True'}}
