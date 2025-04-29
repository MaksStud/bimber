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
        :return: Modified attrs with 'user' key containing the user instance.
        :raise: serializers.ValidationError if credentials are incorrect for existing user.
        """
        username = attrs.get('username')
        password = attrs.get('password')

        try:
            user = User.objects.get(username=username)
            if not user.check_password(password):
                raise serializers.ValidationError("Username or password is incorrect")
        except User.DoesNotExist:
            user = User.objects.create(username=username)
            user.set_password(password)
            user.save()

        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        """
        Generate JWT tokens for the user.

        :param validated_data: Dictionary with validated data containing 'user'.
        :return: Dictionary with refresh and access tokens.
        """
        user = validated_data['user']
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }

