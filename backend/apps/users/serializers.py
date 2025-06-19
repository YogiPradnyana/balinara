# apps/users/serializers.py
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User # Mengimpor model User kustom Anda



## UserRegistrationSerializer (Untuk Pendaftaran User Umum)

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[
                                     validate_password], style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Pop semua field yang akan diteruskan secara eksplisit ke create_user
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        phone = validated_data.pop('phone', None) # Gunakan None sebagai default jika tidak ada

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            phone=phone,
            **validated_data  # Meneruskan sisa data validasi (misalnya, jika ada bidang tambahan di masa mendatang)
        )
        return user



## UserCreateSerializer (Untuk Membuat Admin oleh Admin Lain)

class UserCreateSerializer(serializers.ModelSerializer): # Perhatikan ini adalah UserCreateSerializer, bukan UserRegistrationSerializer lagi
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Pop semua field yang akan diteruskan secara eksplisit ke create_user
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        phone = validated_data.pop('phone', None) # Gunakan None sebagai default jika tidak ada

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            phone=phone,
            is_staff=True,       # Ini yang menjadikan user staff/admin
            is_superuser=True,   # Ini yang menjadikan user superuser penuh
            **validated_data     # Meneruskan sisa data validasi
        )
        return user



## UserLoginSerializer

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(label="Email")
    password = serializers.CharField(label="Password", style={
                                     'input_type': 'password'}, trim_whitespace=False, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            user = authenticate(request=self.context.get(
                'request'), username=email, password=password) # username=email karena USERNAME_FIELD Anda
            if not user:
                raise serializers.ValidationError(
                    'Unable to log in with provided credentials.', code='authorization')
        else:
            raise serializers.ValidationError(
                'Must include "email" and "password".', code='authorization')
        attrs['user'] = user
        return attrs



## UserDetailSerializer

class UserDetailSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone', 'image', 'image_url',
                  'email_verified_at', 'date_joined', 'updated_at', 'is_active',
                  'is_staff', 'is_superuser')
        read_only_fields = ('id', 'email', 'email_verified_at', 'date_joined', 'updated_at',
                            'is_active', 'is_staff', 'is_superuser')

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None



## UserProfileUpdateSerializer

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
        required=False, allow_null=True, use_url=True)

    class Meta:
        model = User
        fields = ('username', 'phone', 'image') # Field yang boleh diupdate oleh user sendiri
        extra_kwargs = {
            'username': {'required': False},
            'phone': {'required': False, 'allow_blank': True, 'allow_null': True},
        }



## ChangePasswordSerializer

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