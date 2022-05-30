"""
Database models.
"""
import os
import uuid

from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models


def recipe_image_file_path(instance, filename):
    """
    Generate file path for new recipe image.

    A function we use to determine the path where we want to store
    our image file
    """
    # Split text function of the path module in order to take the
    # filename and to extract the extension of that filename
    ext = os.path.splitext(filename)[1]
    # Next, let's create our own filename with uuid and append our previous
    # filename to the end of our new filename, so if a user uploads a
    # PNG, JPEG, JPG, the extension will be added to the end.
    filename = f'{uuid.uuid4()}{ext}'

    # Lastly, let's generate the path of our files, with "os.path.join", so
    # no matter what operating system (Windows, Linux, Mac) our server
    # runs on the correct path for the file is created.
    # THIS IS A BEST PRACTICE FOR GENERATING FILEPATHS!
    return os.path.join('uploads', 'recipe', filename)


class UserManager(BaseUserManager):
    """Manager for users"""

    # extra_fields (extra keyword arguments) -> This is useful when adding
    # additional fields to the user model + you don't need to add the fields
    # to the 'create_user' in any other way.
    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address!')
        # DON'T MISSPELL THIS, IT NEEDS TO BE CALLED "user"
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


# PermissionsMixin --> Functionality for the permissions & fields
class User(AbstractBaseUser, PermissionsMixin):

    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Recipe(models.Model):
    """Recipe object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    # IN A REAL PROJECT, USE INTEGER FIELD FOR PRICE VALUES!
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField('Tag')
    ingredients = models.ManyToManyField('Ingredient')
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        return self.title


class Tag(models.Model):
    """Tag for filtering recipes."""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
        )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient for recipes."""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name
