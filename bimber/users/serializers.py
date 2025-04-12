from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class RegistrationLoginSerializer(serializers.ModelSerializer):
    """
    Handles user registration and login.

    - If the user exists and the password is correct — logs in.
    - If the user does not exist — registers a new user.

    Returns:
        - Validated data with 'user' on login.
        - Created user instance on registration.
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'password')

    def validate(self, attrs):
        username = attrs['username']
        password = attrs['password']

        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                attrs['user'] = user
                return attrs
            else:
                raise serializers.ValidationError("Invalid credentials")
        except User.DoesNotExist:
            return attrs

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']

        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_password(password)
            user.save()
        return user
