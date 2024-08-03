
from rest_framework import serializers
from .models import Users, Services, Tickets
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate


def send_activation_email(user):
        subject = 'Save Tax LLC: Activate Your Account'
        activation_link = f"http://example.com/activate/{user.activation_code}"
        message=  f'Hi {user.username},\n\nYour activation code is {user.activation_code}. Use the following link to activate your account: {activation_link}\n\nThanks,\nAdmin'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}
    
    def validate_username(self, value):
        if Users.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username is already taken.")
        return value
    
    def validate_email(self, value):
        if Users.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already taken.")
        return value
    
    def validate_phone_number(self, value):
        if Users.objects.filter(phone_number=value).exists() and value !="":
            raise serializers.ValidationError("Phone number is already taken.")
        return value
    

    def create(self, validated_data):
        user = Users(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            phone_number=validated_data.get('phone_number'),
            referral_code=validated_data.get('referral_code'),
            activation_code=self.generate_unique_activation_code()
        )
    
        user.set_password(validated_data['password'])
        user.save()
        send_activation_email(user)
        return user
    
    def generate_unique_activation_code(self):
        import random
        while True:
            code = random.randint(100000, 999999)
            if not Users.objects.filter(activation_code=code).exists():
                return code
    
    



class CustomTokenObtainPairSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)

        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials")

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tickets
        fields = '__all__'