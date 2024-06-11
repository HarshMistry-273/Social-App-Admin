from rest_framework import serializers
from .models import User, Post, Like, Comment, Follow
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    user = User.objects.filter(is_staff=False)
    class Meta:
        model = User
        exclude = ['is_superuser', 'is_staff', 'groups', 'user_permissions']

class PostSerializer(serializers.ModelSerializer):
    user = User.objects.filter(is_staff=False)
    class Meta:
        model = Post
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    liked_by = serializers.PrimaryKeyRelatedField(queryset = User.objects.filter(is_staff=False) )
    class Meta:
        model = Like
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    comment_user = serializers.PrimaryKeyRelatedField(queryset = User.objects.filter(is_staff=False) )
    class Meta:
        model = Comment
        fields = '__all__'

class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.PrimaryKeyRelatedField(queryset = User.objects.filter(is_staff=False) )
    following = serializers.PrimaryKeyRelatedField(queryset = User.objects.filter(is_staff=False) )
    class Meta:
        model = Follow
        fields = '__all__'

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token    
        fields = ('key',)