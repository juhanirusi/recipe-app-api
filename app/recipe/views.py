"""
Views for the recipe APIs
"""

from core.models import Recipe
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # Override the 'get_queryset' method, so this viewset will show only recipes
    # that the authenticated user requesting the page has made.
    # IT'S BASICALLY AN ADDITIONAL FILTER TO THE 'Recipe.objects.all()' QUERYSET!
    def get_queryset(self):
        """Retrieve recipes for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')
