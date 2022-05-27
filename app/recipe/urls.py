"""
URL mappings for the recipe app.
"""
from django.urls import include, path
# Default router provided by the Django rest_framework
# Use with API view to automatically create routes for all
# different routes available for that view
from rest_framework.routers import DefaultRouter

from recipe import views

# Assign variable 'router' as the DefaultRouter()
router = DefaultRouter()

# Register our viewset with that router, and create a new endpoint
# api/recipes & assign all of the different endpoints from our recipe
# viewset to that endpoint:
# -> AUTOMATICALLY GENERATED URLS DEPENDING ON THE
# FUNCTIONALITY ENABLED ON THE VIEWSET --> supports CRUD + get, post, patch, delete
router.register('recipes', views.RecipeViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),
]
