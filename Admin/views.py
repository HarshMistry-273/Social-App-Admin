from rest_framework import generics
from rest_framework import pagination
from rest_framework import status
from rest_framework import views
from rest_framework import viewsets
from django.contrib.auth import authenticate
from django.db.models import Prefetch
from django.http import JsonResponse, HttpResponse
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from .models import User, Post, Like, Comment, Follow
from .serializers import UserSerializer, PostSerializer, LikeSerializer, CommentSerializer, FollowSerializer,TokenSerializer
from .utils import generate_token

class Analytics(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    def get(self, request):
        try:
            user_count = User.objects.filter(is_staff=False).count()
            inactive_user_count = User.objects.filter(is_staff=False, is_active=False).count()
            post_count = Post.objects.count()
            like_count = Like.objects.count()
            comment_count = Comment.objects.count()
            flagged_comment_count = Comment.objects.filter(is_flagged=True).count()

            return Response({
                'users': user_count,
                'posts': post_count,
                'likes': like_count,
                'comments': comment_count,
                'inactive_users': inactive_user_count,
                'flagged_comments': flagged_comment_count,
            },status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                'ERROR': 'REQUEST NOT EXECUTED',
                'DETAIL': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class DefPagination(pagination.PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 100
        
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
       
class Posts(viewsets.GenericViewSet, generics.mixins.ListModelMixin, generics.mixins.RetrieveModelMixin, generics.mixins.UpdateModelMixin, generics.mixins.DestroyModelMixin):

    serializer_class = PostSerializer
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
                    post_data = PostSerializer(post, context={'request': request}).data                
                    post_data["likes"] = len(post.likes_list)
                    post_data["comments"] = CommentSerializer(post.comments_list, many=True).data

                    data.append(post_data)
                return self.get_paginated_response(data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Comments(viewsets.GenericViewSet, generics.mixins.ListModelMixin, generics.mixins.RetrieveModelMixin, generics.mixins.UpdateModelMixin, generics.mixins.DestroyModelMixin):

    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    pagination_class = DefPagination
    permission_classes = [IsAuthenticated, IsAdminUser]

    @action(detail=False, methods=['get'], url_path='flagged', url_name='flagged')
    def get_all_flagged(self, request):
        try:
            flagged = Comment.objects.filter(is_flagged = True)
            comments = self.get_serializer(flagged, many = True).data

            return Response({
                'FLAGGED': comments
            })
                
        except Exception as e:
            return Response({
            'ERROR': 'REQUEST NOT EXECUTED',
            'DETAIL': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class Likes(viewsets.GenericViewSet, generics.mixins.ListModelMixin, generics.mixins.RetrieveModelMixin):
    serializer_class = LikeSerializer
    queryset = Like.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]

class Login(views.APIView):
    def post(self, request):
        try:
            username = request.data.get("username")
            password = request.data.get("password")

            user = authenticate(username=username, password=password)

            if user:
                if user.is_staff:
                    access_token = AccessToken.for_user(user)
                    return Response(
                        {
                            "ACCESS TOKEN" : str(access_token)
                        }, status=status.HTTP_202_ACCEPTED
                    )
                return Response(
                    {
                        'ERROR': "NON ADMIN USERS CAN'T LOG-IN!"
                    }, status=status.HTTP_403_FORBIDDEN
                )
            return Response({
                "ERROR": "INVALID USERNAME OR PASSWORD"
            }, status=status.HTTP_401_UNAUTHORIZED)
    
        except Exception as e:
            return Response({
            'ERROR': 'REQUEST NOT EXECUTED',
            'DETAIL': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def custom_404_handler(request, exception = None):
    return JsonResponse({
        'status_code': status.HTTP_404_NOT_FOUND,
        'MESSAGE': 'Resource not found!'
    })

class Follows(viewsets.GenericViewSet, generics.mixins.CreateModelMixin):
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()

class ExportUsers(APIView):
    def get(self, request):
        try:
            users = User.objects.all()
            serializer = UserSerializer(users, many = True)

            csv_data = "username,email,firstname,lastname,last_login\n"
            for user in users:
                csv_data+= f"{user.username},{user.email},{user.first_name},{user.last_name},{user.last_login}\n"
            
            response = HttpResponse(csv_data, content_type = 'text/csv')
            response["Content-Disposition"] = 'attachment; filename="users.csv"'
            return response
        
        except Exception as e:
             return Response({
            'ERROR': 'REQUEST NOT EXECUTED',
            'DETAIL': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    












# @api_view(['POST'])
# def login(request):
#     username = request.data.get("username")
#     password = request.data.get("password")

#     if username is None or password is None:
#         return Response({
#             'msg': "Data can't blank" 
#         })
    
#     user = authenticate(request,username=username, password=password)
#     if user is None:
#         return Response({
#             'msg': 'Invalid Creds'
#         })
    
#     token, created = Token.objects.get_or_create(user=user)

#     token_serializer = TokenSerializer(token)
#     serialized_token = token_serializer.data
#     serializer = TokenSerializer(token)
#     if token is None:
#                 return Response({
#             'msg': 'Failed to create Token'
#         })
    
#     return Response({
#         'token': serialized_token
#     })