from rest_framework import serializers
from django.utils.translation import gettext
from django.contrib.auth import get_user_model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    # confirm_password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'password',
            # 'confirm_password'
        )
    def validate(self, attrs):
        return attrs
    
    def validate_email(self, email):
        # user = User.objects.filter(email=attrs.get('email'))
        user = User.objects.filter(email=email)
        if user:
            raise serializers.ValidationError(gettext('User with this email already exists'))
        return email

