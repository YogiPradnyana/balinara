# apps/users/serializers.py
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[
                                     validate_password], style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={
                                      'input_type': 'password'}, label="Confirm password")
    image = serializers.ImageField(
        required=False, allow_null=True, use_url=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password',
                  'password2', 'phone', 'role', 'image')
        extra_kwargs = {
            'phone': {'required': False, 'allow_blank': True, 'allow_null': True},
            'role': {'default': 'user', 'required': False},
        }

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError(
                {"password2": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        if 'image' not in validated_data:  # Handle jika image tidak ada
            validated_data['image'] = None
        # Menggunakan create_user dari CustomUserManager
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(label="Email")
    password = serializers.CharField(label="Password", style={
                                     'input_type': 'password'}, trim_whitespace=False, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            user = authenticate(request=self.context.get(
                'request'), username=email, password=password)
            if not user:
                raise serializers.ValidationError(
                    'Unable to log in with provided credentials.', code='authorization')
        else:
            raise serializers.ValidationError(
                'Must include "email" and "password".', code='authorization')
        attrs['user'] = user
        return attrs


class UserDetailSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone', 'role', 'image', 'image_url',
                  'email_verified_at', 'date_joined', 'updated_at', 'is_active',
                  'is_staff', 'is_superuser')  # Menambahkan info permission
        read_only_fields = ('id', 'email', 'email_verified_at', 'date_joined', 'updated_at',
                            'is_active', 'is_staff', 'is_superuser')

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
        required=False, allow_null=True, use_url=True)

    class Meta:
        model = User
        # Field yang boleh diupdate oleh user sendiri
        fields = ('username', 'phone', 'image')
        extra_kwargs = {
            'username': {'required': False},
            'phone': {'required': False, 'allow_blank': True, 'allow_null': True},
        }


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        required=True, write_only=True, style={'input_type': 'password'})
    new_password = serializers.CharField(required=True, write_only=True, style={
                                         'input_type': 'password'}, validators=[validate_password])
    new_password2 = serializers.CharField(required=True, write_only=True, style={
                                          'input_type': 'password'}, label="Confirm new password")

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct.")
        return value

    def validate(self, data):
        if data.get('new_password') != data.get('new_password2'):
            raise serializers.ValidationError(
                {"new_password2": "New password fields didn't match."})
        return data

    def save(self, **kwargs):
        password = self.validated_data['new_password']
        user = self.context['request'].user
        user.set_password(password)
        user.save(update_fields=['password', 'updated_at'])
        return user
