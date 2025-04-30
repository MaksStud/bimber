from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import AuthorizationSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class AuthorizationView(generics.GenericAPIView):
    """
    API view for user authorization.
    """
    serializer_class = AuthorizationSerializer

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to authorize a user.

        :param request: HTTP request containing 'username' and 'password'.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        :return: Response with access and refresh tokens.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tokens = serializer.save()
        return Response(tokens, status=status.HTTP_200_OK)

