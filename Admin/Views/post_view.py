from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Prefetch
from Admin.models import Post, Like, Comment
from Admin.Serializers import post_serializer, comment_serializer
from Admin.utils import DefPagination

class Posts(viewsets.GenericViewSet, generics.mixins.ListModelMixin, generics.mixins.RetrieveModelMixin, generics.mixins.UpdateModelMixin, generics.mixins.DestroyModelMixin):

    serializer_class = post_serializer.PostSerializer
    queryset = Post.objects.all().order_by('id')
    pagination_class = DefPagination
    # permission_classes = [IsAuthenticated, IsAdminUser]

    def list(self, request):
        try:
            posts = self.filter_queryset(self.get_queryset()).prefetch_related(
                Prefetch('liked_post', queryset=Like.objects.all(), to_attr='likes_list'),
                Prefetch('comment_post', queryset=Comment.objects.all(), to_attr='comments_list')
            )

            page = self.paginate_queryset(posts)

            if page is not None:
                data = []
                for post in page:
                    post_data = post_serializer.PostSerializer(post, context={'request': request}).data                
                    post_data["likes"] = len(post.likes_list)
                    post_data["comments"] = comment_serializer.CommentSerializer(post.comments_list, many=True,  context={'request': request}).data

                    data.append(post_data)
                return self.get_paginated_response(data)
            
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)