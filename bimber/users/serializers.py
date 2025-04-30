from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class AuthorizationSerializer(serializers.Serializer):
    """
    Handles user registration and login.

    - If the user exists and the password is correct — logs in.
    - If the user does not exist — registers a new user and sets the password.

    :param username: Required username string.
    :param password: Required password string.
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """
        Validate user credentials.

        :param attrs: Dictionary containing 'username' and 'password'.
        :return: Modified attrs with 'user'.
        :raise: serializers.ValidationError if credentials are incorrect for existing user.
        """
        username = attrs.get('username')
        password = attrs.get('password')

        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_password(password)
            user.save()
        else:
            if not user.check_password(password):
                raise serializers.ValidationError("Invalid credentials")

        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        """
        Generate JWT tokens for the user.

        :param validated_data: Dictionary with validated data containing 'user'.
        :return: Dictionary with refresh and access tokens.
        """
        user = validated_data.pop('user')

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        return {
            'refresh': str(refresh),
            'access': str(access),
        }
