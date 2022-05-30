"""
Serializers for the user API view.
"""
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext as _
# Import the serializers module from the rest_framework
# Serializers are a way to convert objects to and from python
# objects Takes a JSON input posted from the API & validates
# the input to make sure that it's secure & correct as part of
# validation rules + converts it into a Python object we can use
# or create a model instance to our database
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        # We'll use our user model for this serializer
        model = get_user_model()
        # What fields are available in our serializer
        fields = ['email', 'password', 'name']
        # Give it extra keyword arguments to make the password
        # field readonly. So, the user will be able to set the &
        # save it, but there won't be a value returned from the
        # API response. Also, assign a min_length, if too short it
        # will return a 400 bad request validation error --> The serializer
        # failed the validation cause it didn't meet the criteria defined
        # here & it won't call our 'create' function.
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        # This create method will only be called when
        # the validation is successful.
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)

    # instance -> The instance that's being updated
    # validated_data -> Data that's already been validated
    def update(self, instance, validated_data):
        """
        Override the serializers update method. The update method is
        called whenever we're performing update actions on the
        model that the serializer represents.
        Update and return user.
        """
        # This will retrieve the password from the validated
        # data dictionary and remove it after we've retrieved it,
        # so the view won't show it and the user doesn't have to
        # write their password to change other data
        password = validated_data.pop('password', None)
        # We're only going to overwrite the data that's been changed
        user = super().update(instance, validated_data)

        # If the user is trying to change their password, set the
        # new password as password and save the new password.
        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """
        Validate and authenticate the user.
        Upon POST on the view, the data is posted to the serializer
        & then pass that data to this validator, which will check
        that the data is correct
        """
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        # If username (email) and password don't match with any user
        # in the database then this if statement will get triggered.
        if not user:
            msg = _('Unable to authenticate with provided credentials!')
            raise serializers.ValidationError(msg, code='authorization')

        # If the user was found, we assign our user as the
        # 'user' attribute
        attrs['user'] = user
        return attrs
