from rest_framework import serializers
from .models import User, Post, Like, Comment, Follow
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.HyperlinkedModelSerializer):
    user = User.objects.filter(is_staff=False)
    class Meta:
        model = User
        exclude = ['is_superuser', 'is_staff', 'groups', 'user_permissions']

class PostSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(is_staff=False))

    class Meta:
        model = Post
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PostSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method == 'PUT':
            allowed = ['image', 'caption']
            existing = set(self.fields.keys())
            for field_name in existing - set(allowed):
                self.fields.pop(field_name)

class LikeSerializer(serializers.ModelSerializer):
    liked_by = serializers.PrimaryKeyRelatedField(queryset = User.objects.filter(is_staff=False) )
    class Meta:
        model = Like
        fields = '__all__'

class CommentSerializer(serializers.HyperlinkedModelSerializer):
    comment_user = serializers.PrimaryKeyRelatedField(queryset = User.objects.filter(is_staff=False) )
    class Meta:
        model = Comment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CommentSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method == 'PUT':
            allowed = ['is_flagged']
            existing = set(self.fields.keys())
            for field_name in existing - set(allowed):
                self.fields.pop(field_name)

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