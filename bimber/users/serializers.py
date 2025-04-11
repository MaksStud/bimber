from django.contrib.auth.models import User
from rest_framework import serializers


class RegistrationLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {
            'username': {'validators': []}
        }

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if not username or not password:
            raise serializers.ValidationError("Enter username and password")

        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                attrs['user'] = user
                return attrs
            else:
                raise serializers.ValidationError("Incorrect password")
        except User.DoesNotExist:
            return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user
