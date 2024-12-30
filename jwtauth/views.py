from django.contrib.auth import get_user_model
from rest_framework import decorators, permissions, response, serializers, status
from rest_framework.decorators import api_view, schema
from rest_framework.schemas import AutoSchema
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import CreateAPIView
from .serializers import ResendTokenSerializer, VerificationTokenSerializer, UserCreateSerializer, UserLoginSerializer
from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django.conf import settings

User = get_user_model()


class Registration(CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()

class Login(CreateAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()

    """ def post(self, request):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        return response.Response(serializer.data,status=status.HTTP_200_OK) """

class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Comprueba el password antiguo
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Contraseña equivocada"]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'message': 'La contraseña ha sido cambiada exitosamente',
                'token': str(RefreshToken().for_user(self.object).access_token)
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmailVerificationView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        serializer = VerificationTokenSerializer(data=request.query_params)
        if serializer.is_valid():
            response = {
                "message": "Email validated Succesfully"
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResendVerificationCode(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        serializer = ResendTokenSerializer(data=request.query_params)
        if serializer.is_valid():
            return Response({"message":"codigo reenviado satisfactoriamente"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)