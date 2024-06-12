from rest_framework import status
from rest_framework import views
from django.contrib.auth import authenticate
from django.http import JsonResponse, HttpResponse
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from .models import User, Post, Like, Comment
from .serializers import UserSerializer

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
    
def custom_404_handler(request, exception = None):
    return JsonResponse({
        'status_code': status.HTTP_404_NOT_FOUND,
        'MESSAGE': 'Resource not found!'
    })

# -----------TOKEN AUTH-----------------------------------------------------
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