# apps/users/serializers.py
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User  # Mengimpor model User kustom Anda


# UserRegistrationSerializer (Untuk Pendaftaran User Umum)

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
        # Gunakan None sebagai default jika tidak ada
        phone = validated_data.pop('phone', None)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            phone=phone,
            # Meneruskan sisa data validasi (misalnya, jika ada bidang tambahan di masa mendatang)
            **validated_data
        )
        return user


# UserCreateSerializer (Untuk Membuat Admin oleh Admin Lain)

# Perhatikan ini adalah UserCreateSerializer, bukan UserRegistrationSerializer lagi
class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={
                                     'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Pop semua field yang akan diteruskan secara eksplisit ke create_user
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        # Gunakan None sebagai default jika tidak ada
        phone = validated_data.pop('phone', None)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            phone=phone,
            is_staff=True,       # Ini yang menjadikan user staff/admin
            is_superuser=True,   # Ini yang menjadikan user superuser penuh
            role='admin',
            **validated_data     # Meneruskan sisa data validasi
        )
        return user


# UserLoginSerializer

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(label="Email")
    password = serializers.CharField(label="Password", style={
                                     'input_type': 'password'}, trim_whitespace=False, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            user = authenticate(request=self.context.get(
                # username=email karena USERNAME_FIELD Anda
                'request'), username=email, password=password)
            if not user:
                raise serializers.ValidationError(
                    'Unable to log in with provided credentials.', code='authorization')
        else:
            raise serializers.ValidationError(
                'Must include "email" and "password".', code='authorization')
        attrs['user'] = user
        return attrs


# UserDetailSerializer

class UserDetailSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone', 'image', 'image_url',
                  'email_verified_at', 'date_joined', 'updated_at', 'is_active',
                  'is_staff', 'is_superuser', 'role')
        read_only_fields = ('id', 'email', 'phone', 'email_verified_at', 'date_joined', 'updated_at',
                            'is_active', 'is_staff', 'is_superuser')

    def get_image_url(self, obj):
        print(
            f"    -> SERIALIZER: Memproses data untuk User ID: {obj.id} ({obj.username})")

        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            try:
                # Menambahkan try-except untuk menangkap error saat mengakses .url
                url = obj.image.url
                return request.build_absolute_uri(url) if request else url
            except Exception as e:
                print(
                    f"    !!!!!! ERROR saat mengakses .url untuk User ID: {obj.id}. Error: {e} !!!!!!")
                return None
        return None


# UserProfileUpdateSerializer

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


class UserSimpleSerializer(serializers.ModelSerializer):
    """
    Serializer ringkas untuk menampilkan data user yang tidak sensitif,
    khusus untuk keperluan data bersarang (nested) di dalam review.
    """
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        # Pilih hanya field yang aman dan relevan untuk ditampilkan di samping review
        fields = ['id', 'username', 'image_url']

    def get_image_url(self, obj):
        # Kita gunakan lagi logika yang sama dari UserDetailSerializer Anda
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            try:
                url = obj.image.url
                return request.build_absolute_uri(url) if request else url
            except Exception:
                return None
        return None


# ChangePasswordSerializer

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

class AdminUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Disesuaikan: Hapus 'first_name' dan 'last_name' dari fields
        fields = ['id', 'username', 'email', 'phone', 'is_staff', 'is_active'] # Ganti phone_number menjadi phone
        read_only_fields = ['id'] # ID tidak boleh diubah

    # Opsional: Tambahkan validasi kustom jika diperlukan
    def validate_email(self, value):
        # Pastikan email unik saat update, kecuali untuk instance yang sedang diedit
        if self.instance and User.objects.filter(email=value).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError("Email ini sudah digunakan oleh pengguna lain.")
        return value

    def update(self, instance, validated_data):
        # Disesuaikan: Hapus update untuk first_name dan last_name
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone) # Ganti phone_number menjadi phone
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.save()
        return instance

class AdminSetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True, write_only=True, style={
                                         'input_type': 'password'})
    new_password2 = serializers.CharField(required=True, write_only=True, style={
                                          'input_type': 'password'}, label="Confirm new password")

    def validate(self, data):
        # Validasi kecocokan password tetap ada
        if data.get('new_password') != data.get('new_password2'):
            raise serializers.ValidationError(
                {"new_password2": "New password fields didn't match."})
        return data

    def save(self):
        user = self.context['user'] # User yang akan diubah password-nya
        password = self.validated_data['new_password']
        user.set_password(password)
        user.save(update_fields=['password']) # Sesuaikan jika model User Anda tidak punya updated_at
        return user