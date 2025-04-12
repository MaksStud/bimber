from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegistrationLoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class ApiRegisterLoginView(APIView):
    """
    API endpoint for user registration and login.

    - If user exists and credentials are valid — logs in and returns tokens.
    - If user does not exist — registers a new user and returns tokens.

    Returns:
        - HTTP 200 with tokens on successful login.
        - HTTP 201 with tokens on successful registration.
    """
    def post(self, request):
        serializer = RegistrationLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        if 'user' in validated_data:
            user = validated_data['user']
            status_code = status.HTTP_200_OK
        else:
            user = serializer.save()
            status_code = status.HTTP_201_CREATED

        tokens = self.get_tokens_for_user(user)
        return Response(tokens, status=status_code)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }
