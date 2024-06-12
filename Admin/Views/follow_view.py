from rest_framework import generics
from rest_framework import viewsets
from Admin.models import Follow
from Admin.Serializers import follow_serializer

class Follows(viewsets.GenericViewSet, generics.mixins.CreateModelMixin):
    serializer_class = follow_serializer.FollowSerializer
    queryset = Follow.objects.all()