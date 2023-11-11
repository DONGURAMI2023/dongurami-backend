from .models import User, Item, Badge
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password = validated_data['password']
        )
        return user
    
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'image']
        
    def create(self, validated_data):
        item = Item.objects.create(
            name=validated_data['name'],
            description=validated_data['description'],
            image=validated_data['image']
        )
        return item
    
class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ['id', 'name', 'description', 'image']
        
    def create(self, validated_data):
        badge = Badge.objects.create(
            name=validated_data['name'],
            description=validated_data['description'],
            image=validated_data['image']
        )
        return badge