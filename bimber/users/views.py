from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import AuthorizationSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class AuthorizationView(generics.CreateAPIView):
    """
    API view for user authorization.
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
        
        return Response({
            'access:': str(user.refresh),
            'refresh:': str(user.access)
        }, status=status.HTTP_200_OK)
