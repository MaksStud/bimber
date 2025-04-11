from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegistrationLoginSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken


class ApiRegisterLoginView(APIView):
    def post(self, request):
        serializer = RegistrationLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        if 'user' in validated_data:
            user = validated_data['user']
            token = self.get_tokens_for_user(user)

            return Response({
                "message": "Logged in successfully",
                "username": user.username,
                "access": token['access'],
            }, status=status.HTTP_200_OK)
        else:
            user = serializer.save()
            token = self.get_tokens_for_user(user)

            return Response({
                "message": "User registered successfully",
                "username": user.username,
                "access": token['access'],
            }, status=status.HTTP_201_CREATED)

    def get_tokens_for_user(self, user):
        access_token = AccessToken.for_user(user)
        return {"access": str(access_token)}

