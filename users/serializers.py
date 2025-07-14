from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator

# to return the users data in api response
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email']# include the safe fields only
        
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]# ensure the email is not reused
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]# apply rules for a strong password
    )
    password2 = serializers.CharField(write_only=True, required=True)#hide the password from api responses while confirmi the password
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password2']

    #ensure the passwords thar the user enter are matching 
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])#then transform the password set by the user to a fixed size
        user.save()
        return user# the new user is created and saved to the database
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

