from rest_framework import serializers
from Admin.models import User, Comment

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