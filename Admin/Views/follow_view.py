from rest_framework import generics
from rest_framework import viewsets
from Admin.models import Follow
from Admin.serializers import FollowSerializer

class Follows(viewsets.GenericViewSet, generics.mixins.CreateModelMixin):
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()