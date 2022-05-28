"""
Views for the recipe APIs
"""

from core.models import Recipe, Tag
from rest_framework import mixins, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""
    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # Override the 'get_queryset' method, so this viewset will show only recipes
    # that the authenticated user requesting the page has made.
    # IT'S BASICALLY AN ADDITIONAL FILTER TO THE 'Recipe.objects.all()' QUERYSET!
    def get_queryset(self):
        """Retrieve recipes for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        # If the action is 'list' we return the 'RecipeSerializer'
        # and if it's not we return the serializer
        # configured in the 'serializer_class'
        if self.action == 'list':
            return serializers.RecipeSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """
        Create a new recipe.

        When we create a new recipe through this viewset, we'll call this
        method & assign the user requesting the view as user.
        """
        serializer.save(user=self.request.user)


class TagViewSet(mixins.DestroyModelMixin,
                mixins.UpdateModelMixin,
                mixins.ListModelMixin,
                viewsets.GenericViewSet):
    """Manage tags in the database."""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-name')
