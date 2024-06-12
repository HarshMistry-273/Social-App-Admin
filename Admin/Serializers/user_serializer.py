from rest_framework import serializers
from Admin.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
    user = User.objects.filter(is_staff=False)
    class Meta:
        model = User
        exclude = ['is_superuser', 'is_staff', 'groups', 'user_permissions']