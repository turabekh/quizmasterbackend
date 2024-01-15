from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.password_validation import validate_password
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import serializers


User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'group')

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            group=validated_data.get('group'),
            password=validated_data['password'],
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = User.objects.filter(email=data['email']).first()
        print(user.lockout_until)
        print(user.failed_login_attempts)
        # Check if account is locked
        if user and user.lockout_until and user.lockout_until > timezone.now():
            raise serializers.ValidationError("This account is locked.")

        user = authenticate(email=data['email'], password=data['password'])
        if user and user.is_active:
            # Reset failed login attempts on successful login
            user.failed_login_attempts = 0
            user.lockout_until = None
            user.save()
            return user

        # Increment failed login attempts
        user = User.objects.filter(email=data['email']).first()
        if user:
            user.failed_login_attempts += 1
            if user.failed_login_attempts >= 3:  # Lockout threshold
                user.lockout_until = timezone.now() + timedelta(hours=1)  # Lockout period
            user.save()

        raise serializers.ValidationError("Incorrect Credentials")
    
class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'group']  # Include other fields you want to be updateable
        extra_kwargs = {'group': {'required': False}}  # Make 'group' optional

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        # Update other fields similarly
        if 'group' in validated_data:
            instance.group = validated_data.get('group', instance.group)
        instance.save()
        return instance
    
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        # Check if user exists
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError('User with this email does not exist')

        # Generate token and uid
        self.uid = urlsafe_base64_encode(force_bytes(user.pk))
        self.token = default_token_generator.make_token(user)
        return value

    def save(self, **kwargs):
        # You can include domain and protocol or pass them from the view
        domain = settings.FRONTEND_DOMAIN  # Your React frontend domain
        protocol = 'https' if self.context.get('request').is_secure() else 'http'
        reset_url = f"{protocol}://{domain}/password-reset-confirm/{self.uid}/{self.token}/"

        # Send the email with the custom URL (you need to implement send_reset_email)
        self.send_reset_email(self.validated_data['email'], reset_url)

    def send_reset_email(self, email, reset_url):
        subject = "Password Reset for Your Account"
        message = f"Please click the link below to reset your password:\n{reset_url}"
        email_from = settings.EMAIL_HOST_USER  # Set your email address in settings.py
        recipient_list = [email]
        
        send_mail(subject, message, email_from, recipient_list)

class PasswordResetConfirmSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def validate(self, data):
        try:
            uid = force_str(urlsafe_base64_decode(data['uidb64']))
            self.user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError('Invalid token - user not found')

        if not default_token_generator.check_token(self.user, data['token']):
            raise serializers.ValidationError('Invalid token')

        return data

    def save(self):
        self.user.set_password(self.validated_data['new_password'])
        self.user.save()

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'group']