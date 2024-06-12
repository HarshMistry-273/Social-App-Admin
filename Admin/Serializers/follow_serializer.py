from rest_framework import serializers
from Admin.models import User, Follow

class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.PrimaryKeyRelatedField(queryset = User.objects.filter(is_staff=False) )
    following = serializers.PrimaryKeyRelatedField(queryset = User.objects.filter(is_staff=False) )
    class Meta:
        model = Follow
        fields = '__all__'