from rest_framework import serializers
from django.contrib.auth.models import User
from .models import JobApplication
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class JobApplicationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = JobApplication
        fields = [
            'id', 'user', 'company_name', 'job_title', 'job_url', 
            'status', 'application_date', 'salary_range', 'location',
            'contact_person', 'contact_email', 'interview_date', 
            'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class JobApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = [
            'company_name', 'job_title', 'job_url', 'status', 
            'application_date', 'salary_range', 'location',
            'contact_person', 'contact_email', 'interview_date', 'notes'
        ]

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email', 'first_name', 'last_name']
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False}
        }
    
    def validate(self, attrs):
        """Check that the two password entries match"""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs
    
    def create(self, validated_data):
        """Create user with hashed password"""
        validated_data.pop('password2')  # Remove password2, we don't save it
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

