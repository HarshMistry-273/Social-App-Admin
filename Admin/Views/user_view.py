from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from django.db.models import Prefetch
from rest_framework.response import Response
from Admin.models import User, Post, Like, Comment, Follow
from Admin.serializers import UserSerializer, PostSerializer
from Admin.utils import DefPagination

class Users(viewsets.GenericViewSet, generics.mixins.ListModelMixin, generics.mixins.RetrieveModelMixin, generics.mixins.UpdateModelMixin, generics.mixins.DestroyModelMixin):

    serializer_class = UserSerializer
    queryset = User.objects.filter(is_staff = False).order_by('id')
    pagination_class = DefPagination
    # permission_classes = [IsAuthenticated, IsAdminUser]

    def list(self, request):
        try:
            users = self.filter_queryset(self.get_queryset()).prefetch_related(
                Prefetch('follower', queryset=Follow.objects.all(), to_attr='followers_list'),
                Prefetch('following', queryset=Follow.objects.all(), to_attr='following_list'),
                Prefetch('posts', queryset=Post.objects.prefetch_related(
                    Prefetch('liked_post', queryset=Like.objects.all(), to_attr='likes_list'),
                    Prefetch('comment_post', queryset=Comment.objects.all(), to_attr='comments_list')
                ), to_attr='posts_list')
            )

            page = self.paginate_queryset(users)
            if page is not None:
                data = []
                for user in page:
                    user_data = UserSerializer(user, context={'request': request}).data
                    user_data["followers"] = len(user.followers_list)
                    user_data["following"] = len(user.following_list)

                    posts_data = []
                    for post in user.posts_list:
                        post_data = PostSerializer(post ,context={'request': request}).data
                        post_data["likes"] = len(post.likes_list)
                        post_data["comments"] = len(post.comments_list)
                        posts_data.append(post_data)

                    data.append({
                        'USER': user_data,
                        'POSTS': posts_data
                    })

                return self.get_paginated_response(data)
            
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)