from rest_framework import serializers

from .models import Badge, Item, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'profile_image']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            profile_image = validated_data['profile_image']
        )
        return user
    
    def update(self, validated_data):
        user = User.objects.update(
            email=validated_data['email'],
            username=validated_data['username'],
            profile_image = validated_data['profile_image']
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
