from .models import User, Badge
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password = validated_data['password']
        )
        return user
    
class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = '__all__'
        
    def create(self, validated_data):
        badge = Badge.objects.create(
            name=validated_data['name'],
            description=validated_data['description'],
            image=validated_data['image']
        )
        return badge