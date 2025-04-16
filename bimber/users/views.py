from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import AuthorizationSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class ApiAuthorizationView(generics.CreateAPIView):
    """
    API view for user authorization.

    Processes POST requests with 'username' and 'password'.
    Returns JWT access and refresh tokens for the authenticated user.

    :param request: HTTP request with 'username' and 'password'.
    :return: JSON response containing 'access_token' and 'refresh_token'.
    """
    serializer_class = AuthorizationSerializer

    def create(self, request, *args, **kwargs):
        """
        Create JWT tokens for the authorized user.

        :param request: HTTP request.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        :return: Response object with access and refresh tokens.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        created = serializer.validated_data.get('created', False)
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        return Response({
            'access:': str(access_token),
            'refresh:': str(refresh)
        }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
