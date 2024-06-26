from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from Admin.models import Like
from Admin.Serializers import like_serializer

class Likes(viewsets.GenericViewSet, generics.mixins.ListModelMixin, generics.mixins.RetrieveModelMixin):

    serializer_class = like_serializer.LikeSerializer
    queryset = Like.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]