"""
Views for the user API.
"""
from rest_framework import authentication, generics, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

# Create your views here.
from user.serializers import AuthTokenSerializer, UserSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


# generics.RetrieveUpdateAPIView -> provided by the Django REST Framework
# to provide the functionality needed for retrieving & updating
# objects in the database
class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    # Our update serializer is going to be the same as our create serializer
    # but luckily, the serializer knows which method to use
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    # Make sure that the user that uses this API is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # Override the 'get_object' to return the user who's trying to access
    # the update API page.
    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user
