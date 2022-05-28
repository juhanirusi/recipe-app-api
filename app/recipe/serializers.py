"""
Serializers for recipe APIs
"""

from core.models import Recipe, Tag
from rest_framework import serializers


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

    class Meta:
        model = Recipe
        # Add 'tags' to fields
        fields = ['id', 'title', 'time_minutes', 'price', 'link', 'tags']
        read_only_fields = ['id']

    def _get_or_create_tags(self, tags, recipe):
        """Handle getting or creating tags as needed."""
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

    def create(self, validated_data):
        """Create a recipe."""
        # First, let's assign all tags from data, and assign it to a
        # variable (that's a list) called tags.
        tags = validated_data.pop('tags', [])
        # Then, with rest of the data (excluding tags), we'll create a new
        # recipe with those values
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_tags(tags, recipe)

        return recipe

    # Because we're updating an instance, we need to have 'instance' as a parameter
    def update(self, instance, validated_data):
        """Update recipe."""
        # Let's store the tags in 'tags' variable &
        # if there are no tags set it to 'None'
        tags = validated_data.pop('tags', None)
        # If the 'tags' variable contains tags, we'll clear them and call our
        # '_get_or_create_tags' function
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)

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
        fields = RecipeSerializer.Meta.fields + ['description']
