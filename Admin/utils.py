from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import pagination


def generate_token(user):
    token, created = Token.objects.get_or_create(user=user)
    return token.key

class DefPagination(pagination.PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 100