"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    # Will look at our code and generate the schema
    # file that we need for our project
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    # This URL / view will generate a graphical user
    # interface for our API documentation
    # The 'url_name' will tell the swagger what schema
    # to use (it will use the schema defined above)
    path('api/docs/', SpectacularSwaggerView.as_view(
        url_name='api-schema'), name='api-docs'),
]
