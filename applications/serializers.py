from rest_framework import serializers
from django.contrib.auth.models import User
from .models import JobApplication, UserProfile
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from .models import JobApplication, UserProfile


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
        validators=[UniqueValidator(
            queryset=User.objects.all(), 
            message="This email is already registered"
        )]
    )
    mobile_number = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=15,
        help_text="10-digit Indian mobile number"
    )
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email', 'first_name', 'last_name', 'mobile_number']
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False}
        }
    
    def validate_mobile_number(self, value):
        """Validate mobile number format and uniqueness"""
        if not value:
            return value
        
        # Remove spaces, hyphens, and +91
        clean_number = value.replace(' ', '').replace('-', '').replace('+', '')
        if clean_number.startswith('91'):
            clean_number = clean_number[2:]
        
        # Validate Indian mobile format (10 digits starting with 6-9)
        import re
        if not re.match(r'^[6-9]\d{9}$', clean_number):
            raise serializers.ValidationError(
                "Enter a valid 10-digit Indian mobile number starting with 6-9"
            )
        
        # Check uniqueness
        if UserProfile.objects.filter(mobile_number=clean_number).exists():
            raise serializers.ValidationError(
                "This mobile number is already registered with another account"
            )
        
        return clean_number
    
    def validate(self, attrs):
        """Check that the two password entries match"""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs
    
    def create(self, validated_data):
        """Create user with hashed password and profile"""
        validated_data.pop('password2')
        mobile_number = validated_data.pop('mobile_number', None)
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        
        # Create user profile with mobile number
        UserProfile.objects.create(
            user=user,
            mobile_number=mobile_number if mobile_number else None
        )
        
        return user
