from rest_framework import serializers
from Admin.models import User, Post

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