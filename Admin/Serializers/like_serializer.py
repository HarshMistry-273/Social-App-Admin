
from rest_framework import serializers
from Admin.models import User, Like

class LikeSerializer(serializers.ModelSerializer):
    liked_by = serializers.PrimaryKeyRelatedField(queryset = User.objects.filter(is_staff=False) )
    class Meta:
        model = Like
        fields = '__all__'
