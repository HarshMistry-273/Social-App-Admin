from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from Admin.models import Like
from Admin.serializers import LikeSerializer


class Likes(viewsets.GenericViewSet, generics.mixins.ListModelMixin, generics.mixins.RetrieveModelMixin):

    serializer_class = LikeSerializer
    queryset = Like.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]