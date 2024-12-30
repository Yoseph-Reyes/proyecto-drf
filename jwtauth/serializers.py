from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from core.models.ver_code import VerificationCode
from core.models.reffered import Reffered
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import password_validation, authenticate
from django.contrib.auth.models import User
from django.conf import settings
from core.models.custom_permission import CustomPermission
from core.utils.functions import send_ver_code_email, validate_email_domain
from django.utils import timezone



User = get_user_model()

VALIDATION_DOMAINS = settings.EMAIL_VALIDATION_DOMAINS

class SimpleeDomainRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        # valida si el email contiene el dominio configurado en la constante settings.EMAIL_VALIDATION_DOMAINS
        if not validate_email_domain(value):
            raise serializers.ValidationError("Email does not belong to any of our allowed domain")
        return value

class UserCreateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    about = serializers.CharField(required=False)
    born_date = serializers.DateField()
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=True, style={
                                     "input_type":   "password"})
    password2 = serializers.CharField(
        style={"input_type": "password"}, write_only=True, label="Confirm password")
    is_active = serializers.BooleanField(read_only=True)
    token = serializers.CharField(read_only=True,source='get_token')
    is_staff = serializers.BooleanField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)
    

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "role",
            "about",
            "profile_img",
            "born_date",
            "is_active",
            "is_staff",
            "is_superuser",
            "password",
            "password2",
            "token"
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password")
        password2 = validated_data.pop("password2")
        if password != password2:
            raise serializers.ValidationError(
                {"password": "The two passwords differ."})
        user = User(**validated_data, is_active=False)
        send_ver_code_email(user.email)
        user.set_password(password)
        user.save()

        user_data = User.objects.filter(email = user.email).first()

        CustomPermission.objects.create(user = user_data)

        return user
    
    def get_token(self,obj):
        token = RefreshToken(obj).access_token
        return token
    
    def validate_email(self, value):
        # valida si el email contiene el dominio configurado en la constante settings.EMAIL_VALIDATION_DOMAIN
        if not validate_email_domain(value):
            raise serializers.ValidationError("Email does not belong to any of our allowed domain")
        return value


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, required=True, style={
                                     "input_type":   "password"})
    is_active = serializers.BooleanField(read_only=True)
    token = serializers.SerializerMethodField()
    is_staff = serializers.BooleanField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "role",
            "is_active",
            "is_staff",
            "is_superuser",
            "password",
            "token",
            "partnership"
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):

        # authenticate recibe las credenciales, si son válidas devuelve el objeto del usuario
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Las credenciales no son válidas')

        # Guardamos el usuario en el contexto para posteriormente en create recuperar el token
        self.context['user'] = user
        return data

    def validate_email(self, value):
        # valida si el email contiene el dominio configurado en la constante settings.EMAIL_VALIDATION_DOMAIN
        if not validate_email_domain(value):
            raise serializers.ValidationError("Email does not belong to any of our allowed domain")
        return value

    def create(self, data):
        """Generar o recuperar token."""
        return self.context['user']
    
    def get_token(self,obj):
        refresh = RefreshToken().for_user(obj)
        return {
            "access":str(refresh.access_token),
            "refresh":str(refresh),
            "birth_date": timezone.now(),
            "death_date": timezone.now()+refresh.lifetime,
            }


class ZurichRegisterSerializer(UserCreateSerializer):
    def validate_email(self, value):
        if not value.endswith(f"@zurich.com"):
            raise serializers.ValidationError(f"The email given does not belong to the domain '@zurich.com'")
            
        return value
    
    def create(self, validated_data):
        data = {
            "name":validated_data["first_name"] +" "+ validated_data["last_name"],
            "comision": 0.3,
            "email":validated_data["email"]
        }
        referral = Reffered(**data)
        referral.save()
        return super().create(validated_data)

class ZurichLoginSerializer(UserLoginSerializer):
    def validate_email(self, value):
        if not value.endswith(f"@zurich.com"):
            raise serializers.ValidationError(f"The email given does not belong to the domain '@zurich.com'")
            
        return value
    


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirmed_new_password = serializers.CharField(required=True)

    def validate(self, data):
        if data.get('new_password', None) != data.get('confirmed_new_password', None):
            raise serializers.ValidationError("Las contraseñas no coinciden")
        return data

class VerificationTokenSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=64)

    def validate(self, data):
        try:
            code = VerificationCode.objects.get(code=data.get("code"))
            if code.is_expired():
                raise serializers.ValidationError("The given code expired")

            # If the code is valid then is deleted form the records
            code.delete()
        except VerificationCode.DoesNotExist as e:
            print(e)
            raise serializers.ValidationError("The given code does not match with the records in the DB")
        
        # Activate de account for login
        current_user = User.objects.get(email=code.email)
        current_user.is_active = True
        current_user.save()

        return data
            
class ResendTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, data):
        try:
            current_user = User.objects.get(email=data["email"])
            if current_user.is_active:
                raise serializers.ValidationError("el usuario ya fue validado")
            send_ver_code_email(current_user.email)
        except User.DoesNotExist:
            raise serializers.ValidationError("email invàlido")
        
        return data

