from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class AuthorizationSerializer(serializers.ModelSerializer):
    """
    Handles user registration and login.

    - If the user exists and the password is correct — logs in.
    - If the user does not exist — registers a new user and sets the password.

    :param username: Required username string.
    :param password: Required password string.

    :return: Validated data with 'user' on login or registration.
    """
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'password')

    def validate(self, attrs):
        """
        Validate user credentials.

        :param attrs: Dictionary containing 'username' and 'password'.
        :return: Modified attrs with 'user' key containing the user instance.
        :raise: serializers.ValidationError if credentials are incorrect.
        """
        username = attrs['username']
        password = attrs['password']

        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_password(password)
            user.save()
        else:
            if not user.check_password(password):
                raise serializers.ValidationError("Username or password is incorrect")
        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        """
        Return the user instance from the validated data.

        :param validated_data: Dictionary with validated data containing 'user'.
        :return: User instance.
        """
        return validated_data['user']
